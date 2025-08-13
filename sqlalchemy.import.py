from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Conexão
engine = create_engine('sqlite:///equip.db')
metadata = MetaData()

# Tabela
dados = Table('dados', metadata,
    Column('id', Integer, primary_key=True),
    Column('fonte', String),
    Column('informacao', String),
    Column('valor', Float)
)

metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Função exemplo
def salvar_dado(fonte, informacao, valor):
    ins = dados.insert().values(fonte=fonte, informacao=informacao, valor=valor)
    conn = engine.connect()
    conn.execute(ins)
    conn.close()
    print(f"🔒 Dado salvo: {informacao}")

salvar_dado('Jurídico', 'Processo congestionado', 3000.0) 