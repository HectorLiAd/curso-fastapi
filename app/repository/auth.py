from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.hashing import Hash
from app.db import models
from app.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

def auth_user(usuario, db: Session):
    # usuario = usuario.dict()
    user = db.query(models.User).filter(models.User.username == usuario.username).first()
    # print(user.username)
    if not user:
        
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'No existe el usuario {usuario.username}'
        )
    
    if not Hash.verify_password(usuario.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Contraseña incorrecta'
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

    #return {'res':'login aceptado'}