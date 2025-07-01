from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes
from utils.search import lifespan

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],         
    allow_methods=["*"],           
    allow_headers=["*"],           
)

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI AI backend!"}
