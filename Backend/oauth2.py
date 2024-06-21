# from fastapi import Depends, HTTPException, status
# import JWTtoken
# from fastapi.security import OAuth2PasswordBearer, HTTPBearer

# oauth2_scheme = HTTPBearer()

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return JWTtoken.verify_token(token, credentials_exception)