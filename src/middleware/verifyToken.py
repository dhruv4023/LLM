from fastapi import HTTPException, Header, status
from src.config.appConfig import ENV_VAR, LOG
import jwt

async def verify_token(authorization: str = Header(None)):
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token not provided or invalid")
        
        token = authorization.split("Bearer ")[1]

        try:
            verified = jwt.decode(token, ENV_VAR.JWT_SECRET, algorithms=["HS256"])
            LOG.debug("Token verified successfully")
        except jwt.ExpiredSignatureError:
            LOG.debug("Token expired")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
          
        return verified
    except Exception as e:
        LOG.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
