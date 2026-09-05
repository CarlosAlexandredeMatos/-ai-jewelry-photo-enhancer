from fastapi import APIRouter, Depends, HTTPException
from src.models import Usuario, db
from src.dependencies import get_session
from src.schemas import UsuarioSchema, LoginSchema
from app.app import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
from datetime import datetime, date, timezone, timedelta


auth_router = APIRouter(prefix = '/auth')

def criar_token(id_usuario):
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dic_info = {"sub": id_usuario, "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado



def autenticar_usuario(nome, senha, session):
    usuario = session.query(Usuario).filter(Usuario.nome==nome).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


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


@auth_router.post('/login')
async def login(login_schema: LoginSchema, session = Depends(get_session)):
    usuario = autenticar_usuario(login_schema.nome, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        acess_token = criar_token(usuario.id)
        return {'acess_token': acess_token, 'token_type': 'Bearer'}
