#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regulus Guardian — Supervisor e Restaurador do Projeto

Uso:
  python regulus_guardian.py preflight
  python regulus_guardian.py scan
  python regulus_guardian.py repair [--yes]
  python regulus_guardian.py test
  python regulus_guardian.py backup
  python regulus_guardian.py watch
  python regulus_guardian.py all [--yes]

Variáveis de ambiente (feature flags):
  REGULUS_AUTOFIX=1        # habilita reparos leves por padrão
  REGULUS_DEDUP=1          # habilita deduplicação de arquivos
  REGULUS_RATE=30/60       # 30 chamadas a cada 60s para wrappers rate-limited
  REGULUS_LOG_LEVEL=INFO   # DEBUG, INFO, WARNING, ERROR
"""

import argparse
import ast
import fnmatch
import hashlib
import io
import itertools
import json
import logging
import os
import queue
import shutil
import signal
import sys
import tempfile
import threading
import time
import zipfile
from collections import defaultdict
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# ------------------------ Configuração básica ------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_HINTS = ["RegulusSystemLTDA", "regulus", "src", "backend", "app"]
TEST_DIR_NAME = "tests"
BACKUP_DIR = PROJECT_ROOT / ".rg_backups"
QUARANTINE_DIR = PROJECT_ROOT / ".rg_quarantine"
LOG_DIR = PROJECT_ROOT / ".rg_logs"
LOG_FILE = LOG_DIR / "guardian.log"

DEFAULT_IGNORE = {
    ".git", ".hg", ".svn", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".venv", "venv", "node_modules", ".rg_backups", ".rg_quarantine", ".rg_logs"
}

PYTHON_MIN = (3, 10)

# ------------------------ Logging ------------------------

def setup_logger():
    LOG_DIR.mkdir(exist_ok=True)
    level = os.getenv("REGULUS_LOG_LEVEL", "INFO").upper()
    lvl = getattr(logging, level, logging.INFO)
    logger = logging.getLogger("regulus_guardian")
    logger.setLevel(lvl)
    handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        logger.addHandler(console)
    return logger

log = setup_logger()

# ------------------------ Utilidades ------------------------

def human_bytes(n: int) -> str:
    for unit in ["B","KB","MB","GB","TB"]:
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"

def iter_files(root: Path, patterns=("*",), exts=None):
    for base, dirs, files in os.walk(root):
        # pular diretórios ignorados
        dirs[:] = [d for d in dirs if d not in DEFAULT_IGNORE]
        for f in files:
            if any(fnmatch.fnmatch(f, p) for p in patterns):
                if exts:
                    if Path(f).suffix.lower() in exts:
                        yield Path(base) / f
                else:
                    yield Path(base) / f

def find_source_roots() -> List[Path]:
    roots = []
    for hint in SRC_HINTS:
        p = PROJECT_ROOT / hint
        if p.exists() and p.is_dir():
            roots.append(p)
    if not roots:
        roots.append(PROJECT_ROOT)
    return roots

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def ask_yes_no(msg: str) -> bool:
    try:
        return input(f"{msg} [s/N]: ").strip().lower() in {"s", "sim", "y", "yes"}
    except EOFError:
        return False

# ------------------------ Circuit Breaker / Retry / Rate Limit ------------------------

class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=30):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.state = "CLOSED"
        self.opened_at = None

    def call(self, func, *args, **kwargs):
        now = time.time()
        if self.state == "OPEN":
            if now - (self.opened_at or 0) >= self.reset_timeout:
                self.state = "HALF_OPEN"
            else:
                raise RuntimeError("Circuito aberto — protegendo o sistema.")
        try:
            res = func(*args, **kwargs)
            self.failures = 0
            self.state = "CLOSED"
            return res
        except Exception as e:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
                self.opened_at = now
                log.warning("Circuito aberto após falhas repetidas.")
            raise

def retry(times=3, delay=1.0, backoff=2.0):
    def deco(fn):
        def wrapper(*a, **kw):
            d = delay
            for i in range(times):
                try:
                    return fn(*a, **kw)
                except Exception as e:
                    if i == times - 1:
                        raise
                    log.warning("Falha em %s (tentativa %d/%d): %s; novo try em %.1fs",
                                fn.__name__, i+1, times, e, d)
                    time.sleep(d)
                    d *= backoff
        return wrapper
    return deco

class RateLimiter:
    def __init__(self, tokens:int, period:float):
        self.tokens = tokens
        self.capacity = tokens
        self.period = period
        self.updated = time.time()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            now = time.time()
            # recarregar
            delta = now - self.updated
            refill = (delta / self.period) * self.capacity
            if refill > 0:
                self.tokens = min(self.capacity, self.tokens + refill)
                self.updated = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

def build_rate_limiter():
    # formato "30/60" => 30 chamadas/60s
    spec = os.getenv("REGULUS_RATE", "30/60")
    try:
        tks, per = spec.split("/")
        return RateLimiter(int(tks), float(per))
    except Exception:
        return RateLimiter(30, 60.0)

RATE_LIMITER = build_rate_limiter()
CB = CircuitBreaker()

def rate_limited(fn):
    def wrapper(*a, **kw):
        if not RATE_LIMITER.acquire():
            raise RuntimeError("Rate limit atingido — tente novamente em instantes.")
        return fn(*a, **kw)
    return wrapper

# ------------------------ Pré-voo / Saúde ------------------------

def check_python_version():
    ok = sys.version_info >= PYTHON_MIN
    return ok, f"Python {sys.version.split()[0]} (mínimo {PYTHON_MIN[0]}.{PYTHON_MIN[1]})"

def check_disk_space(path: Path, min_free_gb=1.0):
    total, used, free = shutil.disk_usage(str(path))
    ok = free >= min_free_gb * (1024**3)
    return ok, f"Espaço livre em {path}: {human_bytes(free)} (mín: {min_free_gb}GB)"

def check_structure():
    expected = ["requirements.txt", "README.md"]
    found = []
    for e in expected:
        if (PROJECT_ROOT / e).exists():
            found.append(e)
    roots = find_source_roots()
    return True, f"Raízes de código: {[str(r) for r in roots]}; Achados: {found}"

def preflight():
    checks = [
        ("Versão do Python", check_python_version()),
        ("Disco", check_disk_space(PROJECT_ROOT)),
        ("Estrutura", check_structure()),
    ]
    ok_all = True
    for name, (ok, msg) in checks:
        log.info("[Pré-voo] %s: %s — %s", name, "OK" if ok else "PROBLEMA", msg)
        ok_all &= ok
    return ok_all

# ------------------------ Varredura / Análise ------------------------

def scan_python_files() -> Dict[str, List[str]]:
    """Retorna um dicionário com problemas encontrados por arquivo."""
    problems = defaultdict(list)
    roots = find_source_roots()
    py_files = []
    for r in roots:
        py_files.extend(iter_files(r, patterns=("*.py",)))

    for f in py_files:
        try:
            src = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems[str(f)].append("Codificação inválida (não UTF-8).")
            continue
        try:
            ast.parse(src, filename=str(f))
        except SyntaxError as e:
            problems[str(f)].append(f"SyntaxError L{e.lineno} C{e.offset}: {e.msg}")
        # arquivos vazios/zerados
        if f.stat().st_size == 0:
            problems[str(f)].append("Arquivo vazio (0 bytes).")
        # finais de linha mistos
        if "\r\n" in src and "\n" in src.replace("\r\n", ""):
            problems[str(f)].append("Finais de linha mistos (CRLF/LF).")
        # Byte Order Mark
        if src.startswith("\ufeff"):
            problems[str(f)].append("BOM detectado (U+FEFF).")
    log.info("Varredura: %d arquivos .py analisados", len(py_files))
    return problems

def build_import_graph() -> Dict[str, Set[str]]:
    """Cria um grafo simples de imports (arquivo -> módulos importados)."""
    graph = defaultdict(set)
    roots = find_source_roots()
    for r in roots:
        for f in iter_files(r, patterns=("*.py",)):
            try:
                src = f.read_text(encoding="utf-8")
                tree = ast.parse(src, filename=str(f))
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        graph[str(f)].add(n.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        graph[str(f)].add(node.module.split(".")[0])
    return graph

def find_duplicates(exts=(".py", ".txt", ".md", ".json", ".yaml", ".yml")) -> Dict[str, List[Path]]:
    hashes = defaultdict(list)
    for f in iter_files(PROJECT_ROOT, exts=exts):
        try:
            h = sha256_file(f)
            hashes[h].append(f)
        except Exception:
            continue
    dups = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return dups

# ------------------------ Reparos leves ------------------------

def ensure_packages():
    """Cria __init__.py quando faltar em pacotes (pastas com .py)."""
    created = []
    roots = find_source_roots()
    for r in roots:
        for base, dirs, files in os.walk(r):
            dirs[:] = [d for d in dirs if d not in DEFAULT_IGNORE]
            if any(f.endswith(".py") for f in files):
                initp = Path(base) / "__init__.py"
                if not initp.exists():
                    initp.write_text("# criado automaticamente pelo Regulus Guardian\n", encoding="utf-8")
                    created.append(initp)
    return created

def normalize_file(path: Path):
    """Remove BOM, normaliza EOL para LF."""
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("\ufeff"):
        raw = raw.lstrip("\ufeff")
    raw = raw.replace("\r\n", "\n")
    path.write_text(raw, encoding="utf-8")

def repair(problems: Dict[str, List[str]], auto_yes=False):
    autofix = os.getenv("REGULUS_AUTOFIX", "0") == "1"
    total_fixed = 0
    created_inits = ensure_packages()
    if created_inits:
        log.info("Criados __init__.py em %d pastas.", len(created_inits))
        total_fixed += len(created_inits)

    for file, issues in problems.items():
        p = Path(file)
        do_fix = autofix or auto_yes or ask_yes_no(f"Reparar {file}? {issues}")
        if not do_fix:
            continue
        if any("BOM" in x or "Finais de linha" in x for x in issues):
            try:
                normalize_file(p)
                total_fixed += 1
                log.info("Normalizado %s", file)
            except Exception as e:
                log.error("Falha ao normalizar %s: %s", file, e)
    return total_fixed

def deduplicate(auto_yes=False):
    if os.getenv("REGULUS_DEDUP", "0") != "1":
        log.info("Deduplicação desativada (REGULUS_DEDUP!=1).")
        return 0
    QUARANTINE_DIR.mkdir(exist_ok=True)
    dups = find_duplicates()
    moved = 0
    for h, paths in dups.items():
        # manter o primeiro, mover os demais para quarentena (com índice)
        keep = paths[0]
        for i, p in enumerate(paths[1:], start=1):
            rel = p.relative_to(PROJECT_ROOT)
            target = QUARANTINE_DIR / f"{h[:12]}_{i}__{str(rel).replace(os.sep,'__')}"
            ok = auto_yes or ask_yes_no(f"Duplicado: manter {keep}, mover {p} -> {target}?")
            if not ok:
                continue
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(p), str(target))
                moved += 1
                log.info("Duplicado movido para quarentena: %s", target)
            except Exception as e:
                log.error("Erro ao mover %s: %s", p, e)
    return moved

# ------------------------ Testes ------------------------

def run_tests() -> int:
    import unittest
    test_dir = PROJECT_ROOT / TEST_DIR_NAME
    if not test_dir.exists():
        log.info("Diretório de testes não encontrado: %s (ok, seguindo).", test_dir)
        return 0
    suite = unittest.defaultTestLoader.discover(str(test_dir))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    fails = len(result.failures) + len(result.errors)
    if fails:
        log.error("Testes falharam: %d falhas/erros.", fails)
    else:
        log.info("Todos os testes passaram.")
    return fails

# ------------------------ Backup ------------------------

def make_backup() -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    # hash do estado atual (lista de arquivos + tamanhos) para nomear snapshot
    digest = hashlib.sha256()
    file_list = []
    for f in iter_files(PROJECT_ROOT):
        if any(part in DEFAULT_IGNORE for part in f.parts):
            continue
        try:
            st = f.stat()
        except FileNotFoundError:
            continue
        file_list.append((str(f.relative_to(PROJECT_ROOT)), st.st_size, int(st.st_mtime)))
    for name, size, mtime in sorted(file_list):
        digest.update(f"{name}|{size}|{mtime}".encode("utf-8"))
    short = digest.hexdigest()[:12]
    zpath = BACKUP_DIR / f"snapshot_{stamp}_{short}.zip"
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for f in iter_files(PROJECT_ROOT):
            if any(part in DEFAULT_IGNORE for part in f.parts):
                continue
            z.write(f, arcname=str(f.relative_to(PROJECT_ROOT)))
    log.info("Backup criado: %s (%s)", zpath, human_bytes(zpath.stat().st_size))
    return zpath

# ------------------------ Watcher ------------------------

def watch_loop(interval=2.0, auto_yes=False):
    # mapa path -> (size, mtime)
    state = {}
    def snapshot():
        snap = {}
        for f in iter_files(PROJECT_ROOT):
            if any(part in DEFAULT_IGNORE for part in f.parts):
                continue
            try:
                st = f.stat()
                snap[str(f)] = (st.st_size, int(st.st_mtime))
            except FileNotFoundError:
                continue
        return snap

    state = snapshot()
    log.info("Observando mudanças… (Ctrl+C para parar)")
    try:
        while True:
            time.sleep(interval)
            snap2 = snapshot()
            if snap2 != state:
                log.info("Mudanças detectadas — executando pipeline: scan -> repair -> test")
                probs = scan_python_files()
                repair(probs, auto_yes=auto_yes)
                run_tests()
                state = snap2
    except KeyboardInterrupt:
        log.info("Watcher encerrado.")

# ------------------------ CLI ------------------------

def cmd_preflight(args):
    ok = preflight()
    print("OK" if ok else "PROBLEMAS ENCONTRADOS")
    sys.exit(0 if ok else 1)

def cmd_scan(args):
    probs = scan_python_files()
    graph = build_import_graph()
    print(json.dumps({
        "problemas": probs,
        "import_graph_summary": {k: sorted(list(v))[:10] for k, v in itertools.islice(graph.items(), 0, 50)}
    }, ensure_ascii=False, indent=2))
    if probs:
        log.warning("Problemas detectados em %d arquivos.", len(probs))
        sys.exit(2)

def cmd_repair(args):
    probs = scan_python_files()
    fixed = repair(probs, auto_yes=args.yes)
    moved = deduplicate(auto_yes=args.yes)
    log.info("Reparos: %d alterações; Deduplicados movidos: %d", fixed, moved)

def cmd_test(args):
    fails = run_tests()
    sys.exit(0 if fails == 0 else 3)

def cmd_backup(args):
    make_backup()

def cmd_watch(args):
    watch_loop(interval=args.interval, auto_yes=args.yes)

def cmd_all(args):
    ok = preflight()
    if not ok:
        log.error("Pré-voo falhou — verifique o ambiente.")
        sys.exit(1)
    probs = scan_python_files()
    repair(probs, auto_yes=args.yes)
    deduplicate(auto_yes=args.yes)
    fails = run_tests()
    make_backup()
    if fails == 0:
        log.info("Pipeline concluído com sucesso.")
    else:
        log.error("Pipeline concluiu com falhas de teste (%d).", fails)
        sys.exit(3)

def main():
    parser = argparse.ArgumentParser(description="Regulus Guardian — Supervisor do Projeto")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("preflight").set_defaults(func=cmd_preflight)
    sub.add_parser("scan").set_defaults(func=cmd_scan)

    p_repair = sub.add_parser("repair")
    p_repair.add_argument("--yes", action="store_true", help="Não perguntar; aplicar reparos/dedup automaticamente")
    p_repair.set_defaults(func=cmd_repair)

    sub.add_parser("test").set_defaults(func=cmd_test)
    sub.add_parser("backup").set_defaults(func=cmd_backup)

    p_watch = sub.add_parser("watch")
    p_watch.add_argument("--interval", type=float, default=2.0)
    p_watch.add_argument("--yes", action="store_true")
    p_watch.set_defaults(func=cmd_watch)

    p_all = sub.add_parser("all")
    p_all.add_argument("--yes", action="store_true")
    p_all.set_defaults(func=cmd_all)

    args = parser.parse_args()
    if not getattr(args, "cmd", None):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
