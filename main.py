from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd

app = FastAPI()

@app.on_event("startup")
def startup_event():
    app.state.data_df = None

@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in required_columns):
        raise HTTPException(
            status_code=400,
            detail="Missing required columns"
        )

    app.state.data_df = df
    return {"message": "Data uploaded successfully"}
        
#EP para ver los datos cargados y debuggear
@app.get("/view-data")
async def view_data():
    if app.state.data_df is None:
        return {"message": "No data uploaded yet"}
    
    return {
        "columns": list(app.state.data_df.columns),
        "rows": app.state.data_df.head(5).to_dict() 
    }