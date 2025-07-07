from fastapi import APIRouter, HTTPException, status
from app.models.user import LoginRequest
from app.services.user_service import user_service
from app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/login")
def login(login_data: LoginRequest):
    user = user_service.get_user_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
