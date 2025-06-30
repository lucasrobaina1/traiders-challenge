from fastapi import FastAPI
from app.endpoints import router

app = FastAPI()

@app.on_event("startup")
def startup_event():
    app.state.data_df = None

app.include_router(router)

