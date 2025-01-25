from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

load_dotenv()

from app.database import engine
from app.models import Base
from app.routers.agents import router as agents_router
from app.exceptions import BaseAPIException, ValidationError, ErrorCode

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Homeward Agent API with Postgres")

api_v1 = FastAPI(title="Homeward Agent API v1")

@api_v1.exception_handler(BaseAPIException)
async def base_api_exception_handler(request: Request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )

@api_v1.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for error in exc.errors():
        details.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    validation_error = ValidationError(
        message="Request validation failed",
        details={"validation_errors": details}
    )
    return JSONResponse(
        status_code=validation_error.status_code,
        content=validation_error.to_dict()
    )

@api_v1.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error = BaseAPIException(
        message=exc.detail,
        error_code=ErrorCode.INTERNAL_SERVER_ERROR,
        status_code=exc.status_code
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error.to_dict()
    )

@api_v1.get("/")
def root():
    return {"message": "Welcome to the Agent API"}

api_v1.include_router(agents_router)

app.mount("/api/v1", api_v1)
