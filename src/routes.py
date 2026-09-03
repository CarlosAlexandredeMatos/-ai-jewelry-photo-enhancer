from fastapi import APIRouter

auth_router = APIRouter(prefix = '/auth')

@auth_router.get('/uploads')
async def upload_fotos():
    return 'Foto upada com sucesso'