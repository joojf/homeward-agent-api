You can run it entirely locally, partially in Docker (database only), or fully in Docker (both the web service and the database).

---

## 1. Run Everything Locally

### Steps

1. **Install PostgreSQL** locally

2. **Create a local database & user** (example commands below). Adjust user/password to your liking:
   ```bash
   psql -U postgres -c "CREATE DATABASE agent_db;"
   psql -U postgres -c "CREATE USER user WITH PASSWORD 'password';"
   psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE agent_db TO user;"
   ```

3. **Create a `.env` file** and copy the content from `.env.example` and set the values like this:
   ```bash
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=agent_db
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
   ```
   > If you prefer environment variables directly, set them in your shell or OS environment.  
   > Example: `export DATABASE_URL="postgresql://fastapi_user:fastapi_password@localhost:5432/fastapi_db"`

5. **Install Python dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

6. **Create tables**:
   - We typically rely on `Base.metadata.create_all(bind=engine)` in the code, but if you need to be explicit:
     ```bash
     python -c "from app.models import Base; from app.database import engine; Base.metadata.create_all(bind=engine)"
     ```

7. **Seed the database** (optional):
   ```bash
   python seed_data.py
   ```
   This will load the JSON fixtures (agents, applications, customers) into your local Postgres DB.

8. **Run the app**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive API/OpenAPI docs.

9. **Run tests**:
   ```bash
   pytest app/tests -v
   ```

---

## 2. Run with Database on Docker, Code Locally

### Steps

1. **Install Docker & Docker Compose** if you haven't already.

2. **Start the Postgres container**:
   ```bash
   docker-compose up -d db
   ```
   This will spin up just the Postgres container on `localhost:5432`.

3. **Setup the `.env` file the same way as the first approach** at the project root.

4. **Install Python dependencies** (same as above):
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Seed data** (optional):
   ```bash
   python seed_data.py
   ```

6. **Run the app locally**:
   ```bash
   uvicorn app.main:app --reload
   ```
   - Check [http://localhost:8000/docs](http://localhost:8000/docs).

7. **Stop the DB** if needed:
   ```bash
   docker-compose down
   ```

---

## 3. Run Everything in Docker (Full Containerization)

### Steps

1. **Install Docker & Docker Compose** on your machine.

2. **Setup the `.env` file the same way as the first approach** at the project root.

3. **Build and run**:
   ```bash
   docker-compose build
   docker-compose up
   ```
   - This will spin up **two containers**:
     - **`db`**: The Postgres DB on port `5432`
     - **`web`**: The app on your host's port `8000`.

4. **Seed the data** (optional):
   In a separate terminal:
   ```bash
   docker-compose run web python seed_data.py
   ```

5. **Check the API**:
   - Go to <http://localhost:8000/docs> and explore.

6. **Shut down**:
   ```bash
   docker-compose down
   ```

---

## 4. Testing

Whichever way you run your database, you can test with `pytest`:

- **If running fully local or DB on Docker** + code local:
  ```bash
  pytest app/tests -v
  ```

- You could either run tests inside the container:
     ```bash
     docker-compose run web pytest app/tests -v
     ```
---