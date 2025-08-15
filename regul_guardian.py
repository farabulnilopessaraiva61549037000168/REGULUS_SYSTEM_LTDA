# (opcional) habilitar reparos e dedup automáticos
set REGULUS_AUTOFIX=1 && set REGULUS_DEDUP=1     # Windows (PowerShell: $env:REGULUS_AUTOFIX="1")
export REGULUS_AUTOFIX=1 REGULUS_DEDUP=1         # Linux/macOS

python regulus_guardian.py all --yes

