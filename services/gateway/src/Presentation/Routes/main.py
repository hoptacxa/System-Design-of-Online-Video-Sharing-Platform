from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Presentation.Controllers.dispatch_controller import router as dispatch_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(dispatch_router)

