from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pandas as pd
import os
from sqlalchemy import create_engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Update with your credentials
DB_URL = "postgresql+psycopg2://postgres:12345678@localhost:5432/excel_db"
engine = create_engine(DB_URL)

# This will store the latest dataframe globally
latest_df = pd.DataFrame()

@app.post("/api/upload")
async def upload_excel(file: UploadFile = File(...)):
    global latest_df
    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    df = pd.read_excel(path)
    latest_df = df.copy()  # Save for display

    df.to_sql("excel_data", engine, if_exists="replace", index=False)

    return {"message": "stored", "rows": len(df)}

@app.get("/", response_class=HTMLResponse)
def read_root():
    global latest_df
    if latest_df.empty:
        return "<h3>No Excel uploaded yet.</h3>"

    # Convert first 20 rows to HTML
    html_table = latest_df.head(20).to_html(index=False)
    return f"""
    <html>
        <head>
            <title>Excel Preview</title>
        </head>
        <body>
            <h2>First 20 rows of Excel</h2>
            {html_table}
        </body>
    </html>
    """
