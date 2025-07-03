from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.v1.endpoints import gemini
from app.api.v1.endpoints import collection_points
from app.api.v1.endpoints import user

load_dotenv()

app = FastAPI()


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": f"An unexpected server error occurred: {exc}",
            "data": None,
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(gemini.router, prefix="/api")
app.include_router(collection_points.router, prefix="/api/v1/collection_points")
app.include_router(user.router, prefix="/api/v1/user")


@app.get("/")
def hello():
    return "hello world!"
