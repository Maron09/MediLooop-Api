from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class RegisterResponse(BaseModel):
    success: bool
    message: str
    

class OTPVerify(BaseModel):
    otp_code: str

class NewOTP(BaseModel):
    email: str

class OTPResponse(BaseModel):
    success: bool
    message: str