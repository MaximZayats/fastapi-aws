from fastapi import FastAPI
from fastapi_better_di.patcher.auto import is_pathed
from starlette.responses import RedirectResponse

from application.apps.core.dependencies import setup_dependencies
from application.apps.shared.db import init_db

assert is_pathed(), "Something went wrong"

app = FastAPI()
setup_dependencies(app)


@app.on_event("startup")
async def on_startup() -> None:
    from application.apps.auth.routes import router as auth_router
    from application.apps.core.routes import router as core_router
    from application.apps.data_storage.routes import (
        router as data_storage_router,
    )
    from application.apps.notifications.routes import (
        router as notifications_router,
    )

    app.include_router(auth_router)
    app.include_router(core_router)
    app.include_router(data_storage_router)
    app.include_router(notifications_router)

    await init_db()


@app.get("/")
async def read_root():
    return RedirectResponse("/docs")
