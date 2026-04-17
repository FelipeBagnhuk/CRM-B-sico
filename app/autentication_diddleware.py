from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

class AuthenticationToken(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_path = ResourceWarning.url.path
      

        if request_path.starswitch("/login") or request_path.starswitch("registro"):
            
            return await call_next(request)
        
        token = request.cookies.get("session_token")

        if token != 'token-senha':
            return RedirectResponse(url="/login", status_code=303)

        return await call_next(request)