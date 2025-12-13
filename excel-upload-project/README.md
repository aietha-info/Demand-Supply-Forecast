Step 1: Extract files with directory
    excel-upload-project/
    ├── frontend/
    │   ├── index.html
    │   ├── package.json
    │   ├── vite.config.js
    │   ├── node_modules/
    │   └── src/
    │       ├── App.jsx
    │       ├── main.jsx
    │       └── FileUpload.jsx
    └── backend/
        ├── app.py
        ├── uploads/
        └── __pycache__/

Step 2: Install python and verify

Step 3: Install VS Code setup python env for vs code.
    open the excel-upload-project folder

Step 4: Install frontend dependencies
    bash
        cd frontend
        npm install
        npm install axios
            {Remove existing files and continue
            React
            JavaScript
            and try not to use '@' in passwords}
  
Step 5: Start frontend
    bash
        npm run dev

Step 6: Install backend dependencies
    powershell
        pip install fastapi uvicorn python-multipart pandas openpyxl
    and if you want the FastAPI extras:
        pip install "fastapi[all]"

Step 7: Run backend
    powershell
        uvicorn app:app --reload

Step 8: download postgreSQL and install its dependencies
    powershell
            pip install psycopg2-binary sqlalchemy pandas

Step 9: Add psql to PATH and verify
    css
        psql --version
        psql -U postgres

Step 10: Create a database
    sql
        CREATE DATABASE excel_db;      #here excel_db is used as temp
    
    make sure to edit DB_URL = "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/excel_db"
        temp used as password: 12345678

    To reset password (without login)
        powershell
            psql -U postgres
    (if logged in)
        sql
            ALTER USER postgres WITH PASSWORD 'new_password';
        and update the same for DB_URL

Step 11: 
1. can check the data in DB
    powershell
        psql -U postgres -h localhost -d excel_db
    sql
        \dt
        SELECT * FROM excel_data;               #here excel_data was uploaded as test
    exit sql
        \q


2. Using pgAdmin (GUI)

Open pgAdmin (installed with PostgreSQL).

Connect to server localhost, login with postgres user and password.

Expand Databases → excel_db → Schemas → public → Tables.

Right-click table → View/Edit Data → All Rows.

This gives a full GUI view of your DataFrame.

3. Using python
python
    import pandas as pd
    from sqlalchemy import create_engine

    engine = create_engine("postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/excel_db")
    df = pd.read_sql("SELECT * FROM excel_data", engine)
    print(df)
