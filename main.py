from fastapi import FastAPI
from app.endpoints import router
from app.logger import setup_logging

# Configurar logging antes de crear la app
setup_logging()

app = FastAPI()

@app.on_event("startup")
def startup_event():
    app.state.data_df = None

app.include_router(router)

