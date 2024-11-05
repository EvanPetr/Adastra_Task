from fastapi import FastAPI
from app.cars.api import router_car
from app.auth.api import router_auth
from app.users.api import router_user
from app.database import engine, Base
from fastapi_pagination import add_pagination

app = FastAPI()
app.include_router(router_car)
app.include_router(router_auth)
app.include_router(router_user)
add_pagination(app)

Base.metadata.create_all(bind=engine)
