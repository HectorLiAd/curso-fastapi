from sqlite3 import connect
from urllib import response
from fastapi.testclient import TestClient
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(SCRIPT_DIR), '../'))
from main import app
from app.db.database import SQLALCHEMY_DATABASE_URL 
from app.db.models import Base
from app.hashing import Hash
from app.db.database import get_db
db_path = os.path.join(os.path.dirname(__file__), 'test.db')
db_uri = "sqlite:///{}".format(db_path)

SQLALCHEMY_DATABASE_URL = db_uri

engine_test = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})
TestingSessionLocal = sessionmaker(bind=engine_test,autocommit=False,autoflush=False)
Base.metadata.create_all(bind=engine_test)

cliente = TestClient(app)

def insertar_usuario_prueba():    
    password_hash = Hash.hash_password('pruebapwd')

    engine_test.execute(
        f"""
        INSERT INTO usuario
        (username, password, nombre, apellido, direccion, telefono, correo)
        VALUES('prueba01', '{password_hash}', 'prueba01', 'prueba01', 
        'prueba01', 'prueba01', 'prueba01')
        """
    )


insertar_usuario_prueba()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_crear_usuario():
    # time.sleep(2)
    usuario = {
        "username": "prueba",
        "password": "string",
        "nombre": "string",
        "apellido": "string",
        "direccion": "string",
        "telefono": 0,
        "correo": "string",
        "creacion_user": "2022-09-17T17:16:25.952687"
    }

    response = cliente.post('/user/',json=usuario)
    assert response.status_code == 401
    usuario_login = {
        "username": "prueba01",
        "password": "pruebapwd"
    }
    response_token = cliente.post('/login/',data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()['token_type'] == 'bearer'


    headers = {
        'Authorization': f'Bearer {response_token.json()["access_token"]}'
    }
    print(headers)
    print(response_token.json())

    response = cliente.post('/user/',json=usuario,headers=headers)
    print(response.json())

    assert response.status_code == 201
    assert response.json()['respuesta'] == 'Usuario creado correctamente!!'
    # assert response.json()['respuesta'] == 'Usuario creado correctamente!!'

def test_obtener_usuarios():
    usuario_login = {
        "username": "prueba01",
        "password": "pruebapwd"
    }
    response_token = cliente.post('/login/',data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()['token_type'] == 'bearer'


    headers = {
        'Authorization': f'Bearer {response_token.json()["access_token"]}'
    }
    response = cliente.get('/user/', headers=headers)
    print(response.json())


def test_obtener_usuario():
    response = cliente.get('/user/1')
    print(response.json())
    assert response.json()['username'] == 'prueba01'

def test_eliminar_usuario():
    response = cliente.delete('/user/1')
    assert response.json()['respuesta'] == 'Usuario eliminado'
    print(response.json())

    response = cliente.get('/user/1')
    assert response.json()['detail'] == 'No existe el usuario con el id 1'
    print(response.json())


def test_actualizar_usuario():
    usuario = {
        "username": "prueba_modificado"
    }
    response = cliente.patch('/user/2', json=usuario)
    assert response.json()['respuesta'] == 'Usuario actualizado'
    print(response.json())

    response_user = cliente.get('/user/2')
    assert response_user.json()['username'] == 'prueba_modificado'
    assert response_user.json()['nombre'] == 'string'
    print(response_user.json())


def test_no_encuentra_usuario():
    usuario = {
        "username": "prueba_modificado"
    }
    response = cliente.patch('/user/12', json=usuario)
    print(response.json())
    assert response.json()['detail'] == 'No  existe el usuario con el id 12'

def test_delete_database():
    db_path  = os.path.join(os.path.dirname(__file__), 'test.db')
    os.remove(db_path)
