from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base


#Cria a conexão do banco
db = create_engine('sqlite:///banco.db')

#Cria a base do banco
Base = declarative_base()

#Cria classes e tabelas do banco
class usuarios(Base):
    __tablename__ = 'usuario'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    senha = Column('senha', String, nullable=False)
    admin = Column('admin', Boolean, nullable=False, default=False)
    ativo = Column('ativo', Boolean, nullable=False, default=True)

    def __init__(self, nome, senha, ativo=True, admin=False):
        self.nome = nome
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Joias(Base):
    __tablename__ = 'joia'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    usuario_id = Column('usuario_id', Integer, ForeignKey('usuario.id'))
    imagem_original = Column('imagem_original', String, nullable=False)
    imagem_processada = Column('imagem_processada', Boolean, nullable=False, default=False)
    data_criacao = Column('data_criacao', Boolean, nullable=False, default=True)



    def __init__(self, usuario_id, imagem_original, imagem_processada, data_criacao):
        self.usuario_id = usuario_id
        self.imagem_original = imagem_original
        self.imagem_processada = imagem_processada
        self.data_criacao = data_criacao

#Executa a criação das tabelas
# Base.metadata.create_all(db)
