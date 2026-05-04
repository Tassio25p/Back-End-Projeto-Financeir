from pydantic import BaseModel, EmailStr, Field


# Dados recebidos no login
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=6, max_length=72)


# Resposta enviada após login bem-sucedido
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Solicitação para recuperar senha
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# Verificação do PIN enviado por e-mail
class VerifyPinRequest(BaseModel):
    email: EmailStr
    pin: str = Field(min_length=6, max_length=6)


# Redefinição de senha usando PIN
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    pin: str = Field(min_length=6, max_length=6)
    nova_senha: str = Field(min_length=6, max_length=72)