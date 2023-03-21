from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users
from utils.faces import FindFace
app = FastAPI(openapi_url="/api/v1/openapi.json",
              docs_url="/api/v1/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)



app.include_router(users.router, prefix='/api/v1')
