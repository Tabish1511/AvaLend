from fastapi import APIRouter, HTTPException, Depends, status
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from models import Token, CreateUserRequest, Users
from fastapi.security import OAuth2PasswordRequestForm
from auth import bcrypt_context, authenticate_user, create_access_token
from database import engine

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

def get_db():
    with Session(engine) as session:
        yield session

db_dependency = Annotated[Session, Depends(get_db)]

# FIRST TIME SIGNUP
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, User: CreateUserRequest):
    new_user = Users(
        username=User.username,
        hashed_password=bcrypt_context.hash(User.password),
    )
    db.add(new_user)
    db.commit()

# ALREADY HAVE AN ACCOUNT / LOGIN
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    existing_user = authenticate_user(form_data.username, form_data.password, db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token = create_access_token(existing_user.username, existing_user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}

