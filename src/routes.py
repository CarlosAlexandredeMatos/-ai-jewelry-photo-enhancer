from fastapi import APIRouter
from src.models import Usuario, db
from sqlalchemy.orm import sessionmaker


auth_router = APIRouter(prefix = '/auth')

@auth_router.get('/')
async def home():
    return 'Autenticado com sucesso!'


@auth_router.post('/cadastrar_usuario')
async def cadastrar_usuario(nome: str, senha: str):
    Session = sessionmaker(bind = db)
    session = Session()

    usuario = session.query(Usuario).filter(Usuario.nome == nome).all()
    if usuario:
        return 'Erro, já existe um usuario com este nome.'

    else:
        novo_usuario = Usuario(nome, senha)
        session.add(novo_usuario)
        session.commit()

        return 'Usuário cadastrado com sucesso'