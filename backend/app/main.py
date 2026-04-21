from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.users import user_router

app = FastAPI(title="Employee Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(user_router)
