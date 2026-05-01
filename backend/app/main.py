from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.seeder import runSeeder
from app.routers.users import user_router
from app.routers.auth import auth_router
from app.routers.positions import position_router
from app.routers.employees import employee_router
from app.routers.service_types import service_type_router
from app.routers.service_orders import service_order_router

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


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(position_router)
app.include_router(employee_router)
app.include_router(service_type_router)
app.include_router(service_order_router)

# runSeeder()
