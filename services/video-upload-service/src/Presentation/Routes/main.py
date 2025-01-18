from fastapi import FastAPI
from Presentation.Controllers.video_upload_controller import router as video_upload_router
from Infrastructure.Repositories.database_engine import DatabaseEngine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_engine = DatabaseEngine()
    database_engine.create_db_and_tables()
    app.dependency_overrides[DatabaseEngine] = lambda: database_engine
    
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(video_upload_router)

