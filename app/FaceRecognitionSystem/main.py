import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import customers, auth,accounts,faces
from fastapi import FastAPI
from sockets import sio_app

app = FastAPI(openapi_url="/api/v1/openapi.json",
              docs_url="/api/v1/docs",
              )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(customers.router, prefix='/api/v1')
app.include_router(auth.router, prefix='/api/v1')
app.include_router(accounts.router, prefix='/api/v1')
app.include_router(faces.router, prefix='/api/v1')

app.mount('/', app=sio_app)
