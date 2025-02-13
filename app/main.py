from fastapi import FastAPI
from sqlmodel import SQLModel
from db.session import engine
from db.models.tablemodel import TableModel
from core.config import Settings
from db.models import product, user,category
from routes import router
from middlewares.cors import add_cors_middleware

#TableModel.metadata.create_all(engine)

def include_router(app):
    app.include_router(router)


def start_application():
    app = FastAPI(
        title=Settings.PROJECT_NAME,
        version=Settings.PROJECT_VERSION,
        description=Settings.PROJECT_DESCRIPTION
    ) 
    add_cors_middleware(app)
    include_router(app)
    return app

app = start_application()


@app.get("/")
def read_root():
    return {"message": "FastAPI app!"}