from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_database
from .routers import clientes, terrenos
from .routers import contratos, pagamentos


def create_app() -> FastAPI:
    app = FastAPI(title="Imobiliaria API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(clientes.router, prefix="/api/clientes", tags=["clientes"])
    app.include_router(terrenos.router, prefix="/api/terrenos", tags=["terrenos"])
    app.include_router(contratos.router, prefix="/api/contratos", tags=["contratos"])
    app.include_router(pagamentos.router, prefix="/api/pagamentos", tags=["pagamentos"])

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


create_database()
app = create_app()

