from wsgiref.simple_server import demo_app
from app.db import models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.hashing import Hash





def crear_usuario(user, db: Session):
    usuario = user.dict()
    try:
        nuevo_usuario = models.User(
            username = usuario['username'],
            password = Hash.hash_password(usuario['password']),
            nombre = usuario['nombre'],
            apellido = usuario['apellido'],
            direccion = usuario['direccion'],
            telefono = usuario['telefono'],
            correo = usuario['correo']
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return {"respuesta":"Usuario creado correctamente!!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = f'Error creando usuario {e}'
        )

def obtener_usuario(user_id, db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id}"
        )
    return usuario.first()

def eliminar_usuario(user_id, db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No existe el usuario con el id {user_id}'
        )
    usuario.delete(synchronize_session=False)
    db.commit()
    return {"respuesta":"Usuario eliminado"}

def obtener_usuarios(db:Session):
    return db.query(models.User).all()

def actualizar_usuario(user_id, updateUser, db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'No  existe el usuario con el id {user_id}'
        )    
    usuario.update(updateUser.dict(exclude_unset=True))
    db.commit()
    return {"respuesta":"Usuario actualizado"}