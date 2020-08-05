import os
import secrets
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.db.session import SessionLocal

security = HTTPBasic()


def get_db() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    correct_username = secrets.compare_digest(
        credentials.username, os.getenv("USERNAME"))
    correct_password = secrets.compare_digest(
        credentials.password, os.getenv("PASSWORD"))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
