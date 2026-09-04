from fastapi import APIRouter, Depends
from src.models import Usuario, db
from dependencies import get_session

auth_router = APIRouter(prefix = '/auth')

@auth_router.get('/')
async def home():
    return 'Autenticado com sucesso!'


@auth_router.post('/cadastrar_usuario')
async def cadastrar_usuario(nome: str, senha: str, session = Depends(get_session)):
    session = get_session()
    usuario = session.query(Usuario).filter(Usuario.nome == nome).all()
    if usuario:
        return 'Erro, já existe um usuario com este nome.'

    else:
        novo_usuario = Usuario(nome, senha)
        session.add(novo_usuario)
        session.commit()

        return 'Usuário cadastrado com sucesso'