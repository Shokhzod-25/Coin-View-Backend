from pydantic import BaseModel, EmailStr, ConfigDict


class UserRegister(BaseModel):
    user_name: str
    password: str
    first_name: str
    email: EmailStr
    phone_number: str

class UserLogin(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None
    user_name: str | None = None
    password: str


class ResponseAccessRefreshTokenRegister(BaseModel):
    access_token: str
    refresh_token: str


class ResponseAccessRefreshTokenLogin(BaseModel):
    access_token: str
    refresh_token: str
    api_key: str | None = None


class ResponseRegisterUser(BaseModel):
    id: int
    email: EmailStr
    phone_number: str
    first_name: str
    user_name: str

    model_config = ConfigDict(from_attributes=True)

class ResponseLoginUser(BaseModel):
    id: int
    email: EmailStr
    phone_number: str
    first_name: str
    user_name: str
    req_count: int
    api_key: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ResponseCurrentUser(BaseModel):
    id: int
    email: EmailStr
    phone_number: str
    first_name: str
    user_name: str
    req_count: int | None = None
    api_key: str | None = None

    model_config = ConfigDict(from_attributes=True)
