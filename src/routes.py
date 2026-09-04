from fastapi import APIRouter, Depends, HTTPException
from src.models import Usuario, db
from src.dependencies import get_session
from src.schemas import UsuarioSchema
from app.app import bcrypt_context


auth_router = APIRouter(prefix = '/auth')

@auth_router.get('/')
async def home():
    return 'Autenticado com sucesso!'


@auth_router.post('/cadastrar_usuario')
async def cadastrar_usuario(usuario_schema: UsuarioSchema, session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.nome == usuario_schema.nome).all()
    if usuario:
        raise HTTPException(400,'Erro, já existe um usuario com este nome.')

    else:
        senha_cript = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, senha_cript)
        session.add(novo_usuario)
        session.commit()

        return 'Usuário cadastrado com sucesso'