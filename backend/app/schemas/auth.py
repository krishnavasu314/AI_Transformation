from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResult(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict
