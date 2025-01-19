from fastapi import FastAPI
from Presentation.Controllers.dispatch_controller import router as dispatch_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(dispatch_router)

