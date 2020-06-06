from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.mongodb import db

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_event_handler("startup", db.connect_to_mongo)
app.add_event_handler("shutdown", db.close_mongo_connection)


if __name__ == "__main__":
    import uvicorn

    from app.initial_data import main as main_initial_data

    db.connect_to_mongo()

    main_initial_data()

    db.close_mongo_connection()

    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
