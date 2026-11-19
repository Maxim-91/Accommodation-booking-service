# Backend Documentation

## Accommodation Booking Service

This document describes how to install, configure, run, and test the backend of the Accommodation Booking Service project.

It is intended for developers who want to set up the project locally and understand the main backend development workflow.

## 1. Requirements

Before starting, make sure the following software is installed:

- Python — use the version specified in the project's CI configuration.
- PostgreSQL.
- Git.
- A code editor or IDE, such as Visual Studio Code or PyCharm.

The following tools are optional but useful:

- pgAdmin 4 — for managing PostgreSQL databases.
- Docker Desktop — for running services in containers.
- GitHub Desktop — for managing branches and commits.

## 2. Installation

### Step 1. Clone the repository

Open PowerShell and run:

```powershell
git clone https://github.com/Maxim-91/Accommodation-booking-service.git
```

Navigate to the project directory:

```powershell
cd Accommodation-booking-service
```

### Step 2. Open the Backend directory

```powershell
cd Backend
```

Run the following commands from this directory unless stated otherwise.

### Step 3. Create a virtual environment

```powershell
python -m venv .venv
```

### Step 4. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the virtual environment again.

### Step 5. Install dependencies

Install the main project dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the repository contains `requirements-dev.txt`, install development dependencies as well:

```powershell
python -m pip install -r requirements-dev.txt
```

The virtual environment keeps the project's Python packages separate from other Python installations.

## 3. Environment Configuration

The backend uses environment variables to configure database connections and application security.

### 3.1. Required environment variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string used by the application and database migrations |
| `TEST_DATABASE_URL` | PostgreSQL connection string used by integration tests |
| `TOKEN_KEY` | Secret key used for token-related security |

A PostgreSQL connection string has the following format:

```text
postgresql+psycopg2://username:password@127.0.0.1:5432/database_name
```

Replace the example values with your local PostgreSQL credentials and database name.

### 3.2. Configure environment variables in PowerShell

For local development, configure the variables in your PowerShell session:

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://accommodation_user:YOUR_PASSWORD@127.0.0.1:5432/accommodation_db"

$env:TEST_DATABASE_URL = "postgresql+psycopg2://accommodation_user:YOUR_PASSWORD@127.0.0.1:5432/accommodation_db_test"

$env:TOKEN_KEY = "your-local-secret-key"
```

Replace `YOUR_PASSWORD` and the secret key with your own values.

These variables remain available only in the current terminal session. If you open another PowerShell window, configure them again.

**Important:** The integration test helper reads `TEST_DATABASE_URL`. The `.env.test` file is not automatically loaded by Python's `unittest` runner, so set this variable before running integration tests.

### 3.3. Environment file security

You may use local `.env` and `.env.test` files for configuration if the application or test setup loads them.

Never commit files containing real passwords, database credentials, or secret keys.

An `.env.example` file may be included in the repository to show the required variable names without exposing real credentials.

## 4. PostgreSQL Database Setup

The backend uses PostgreSQL for persistent application data.

You need a running PostgreSQL server and two separate databases.

### Step 1. Create the development database

Create a database named:

```text
accommodation_db
```

This database is used for local application development.

### Step 2. Create the test database

Create another database named:

```text
accommodation_db_test
```

This database is used by integration tests.

You can create both databases using pgAdmin 4 or another PostgreSQL client.

### Step 3. Configure database connections

Set `DATABASE_URL` to the development database and `TEST_DATABASE_URL` to the test database.

**Important:**

- Do not run integration tests against the development or production database.
- The test database must be separate.
- The integration test helper checks that the test database name ends with `_test`.
- Database tables should be created and updated using Alembic migrations, not manually.

## 5. Database Migrations

The project uses SQLAlchemy for database interaction and Alembic for database schema migrations.

Run Alembic commands from the `Backend` directory with `DATABASE_URL` configured.

### 5.1. Check the current migration

```powershell
alembic current
```

Displays the migration revision currently applied to the database.

### 5.2. View migration history

```powershell
alembic history
```

Displays the available migration history.

### 5.3. Apply all migrations

```powershell
alembic upgrade head
```

Applies all available migrations up to the latest revision.

Run this command when setting up a new database or updating an existing database.

### 5.4. Create a new migration

After changing SQLAlchemy models, generate a migration:

```powershell
alembic revision --autogenerate -m "describe your change"
```

For example:

```powershell
alembic revision --autogenerate -m "add accommodation fields"
```

Alembic compares the model metadata with the current database schema and generates a migration file in the migration versions directory.

**Always review the generated migration before applying it.** Autogeneration may not correctly detect every change. For example, renaming a column may be interpreted as dropping the old column and creating a new one, which can result in data loss.

### 5.5. Apply the new migration

```powershell
alembic upgrade head
```

### 5.6. Roll back the latest migration

```powershell
alembic downgrade -1
```

This reverts the latest migration.

After checking the rollback, apply the latest migration again:

```powershell
alembic upgrade head
```

Always review migration changes before applying them to a database containing important data.

## 6. Running the Backend

Make sure that:

- You are in the `Backend` directory.
- The virtual environment and dependencies are available.
- PostgreSQL is running.
- `DATABASE_URL` is configured.
- Database migrations have been applied.

Start the FastAPI application:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

The `--reload` option automatically restarts the development server when source files change.

To stop the server, press `CTRL + C` in the terminal.

## 7. API Documentation and Testing

FastAPI automatically generates interactive API documentation.

After starting the backend, open:

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/docs` | Interactive Swagger UI |
| `http://127.0.0.1:8000/redoc` | ReDoc documentation |
| `http://127.0.0.1:8000/openapi.json` | OpenAPI specification |

### 7.1. Test API endpoints using Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

To test an endpoint:

1. Find the endpoint in the list.
2. Expand it.
3. Click **Try it out**.
4. Enter the required parameters or request body.
5. Click **Execute**.
6. Review the response status code and response body.

Swagger UI displays the endpoints registered in the application, including their HTTP methods, parameters, request schemas, and response schemas.

### 7.2. Authentication

For endpoints that require authentication, obtain a token using the appropriate authentication endpoint.

If Bearer authentication is enabled in the API documentation, use the **Authorize** button in Swagger UI and enter the token in the required format.

Follow the authentication requirements displayed by the actual API documentation.

## 8. Automated Tests

The project uses Python's built-in `unittest` framework.

Tests are organized into three categories:

| Test category | Purpose |
|---|---|
| Unit tests | Test individual functions and business logic |
| API tests | Test HTTP endpoints and request/response behaviour |
| Integration tests | Test interaction with the PostgreSQL database |

Unit tests may use an in-memory SQLite database, while integration tests use a separate PostgreSQL test database.

SQLite and PostgreSQL behave differently in some areas, so integration tests are important for verifying database behaviour against the actual database system.

### 8.1. Configure the test environment

Before running integration tests, configure:

```powershell
$env:TEST_DATABASE_URL = "postgresql+psycopg2://accommodation_user:YOUR_PASSWORD@127.0.0.1:5432/accommodation_db_test"

$env:TOKEN_KEY = "test-only-secret-key"
```

Make sure the PostgreSQL server is running and the test database exists.

### 8.2. Run unit tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests\unit -v
```

### 8.3. Run API tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests\api -v
```

### 8.4. Run integration tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests\integration -v
```

Integration tests require a working PostgreSQL connection and the `TEST_DATABASE_URL` variable.

### 8.5. Run all tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

A successful test run finishes with:

```text
OK
```

If tests fail, review the error message and traceback to identify the cause.

Do not consider the test suite successful if required tests report errors or failures.

## 9. Continuous Integration

The project uses GitHub Actions to automate backend checks.

The workflow configuration is located in:

```text
.github/workflows/ci.yml
```

The workflow is configured to run for the GitHub events specified in its configuration, such as pushes and pull requests targeting the `main` branch.

The CI workflow can perform the following steps:

1. Check out the repository.
2. Set up the required Python version.
3. Install project dependencies.
4. Start a PostgreSQL service for integration tests.
5. Configure the required environment variables.
6. Run automated tests.
7. Report the workflow result.

To check the results:

1. Open the project repository on GitHub.
2. Select the **Actions** tab.
3. Open the latest workflow run.
4. Review the results of each job and step.

A successful CI run indicates that the configured automated checks have passed in the CI environment.

## 10. Development Workflow

The project uses Git and GitHub for version control and collaboration.

Development work should follow a feature-branch workflow:

1. Update the local `main` branch.
2. Create a separate branch for the task.
3. Implement the changes.
4. Run the relevant tests locally.
5. Commit the changes with a descriptive message.
6. Push the branch to GitHub.
7. Create a Pull Request targeting `main`.
8. Review the code and CI results.
9. Merge the Pull Request after the required checks pass.

For more information about branches, commits, and Pull Requests, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 11. Security Guidelines

Follow these rules when working with the backend:

- Never commit passwords, database credentials, or secret keys.
- Keep `.env` and `.env.test` files out of version control.
- Do not commit the `.venv/` directory.
- Do not commit Python cache files.
- Use a separate PostgreSQL database for integration tests.
- Never run automated tests against a production database.
- Keep project dependencies listed in the appropriate requirements files.
- Review database migrations before applying them.
- Do not expose sensitive information in API responses or logs.

The `.gitignore` file should exclude local configuration files and generated Python files.

Example entries:

```gitignore
.venv/
__pycache__/
*.pyc
.env
.env.test
```

Review the existing `.gitignore` before adding new entries.

## 12. Troubleshooting

### PowerShell blocks virtual environment activation

Run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Python or pip is not recognized

Check that Python is installed and available:

```powershell
python --version
```

You can also use the virtual environment's Python executable:

```powershell
.\.venv\Scripts\python.exe --version
```

### A required Python package is missing

Install the project dependencies again:

```powershell
python -m pip install -r requirements.txt
```

### PostgreSQL connection fails

Check that:

- PostgreSQL is running.
- The database exists.
- The username and password are correct.
- The host and port are correct.
- The connection string points to the intended database.
- The required environment variable is configured.

### Integration tests cannot connect to PostgreSQL

Check the test database variable:

```powershell
$env:TEST_DATABASE_URL
```

Make sure it points to the separate test database and that the database name ends with `_test`.

### Alembic cannot connect to the database

Check `DATABASE_URL` and verify the connection:

```powershell
alembic current
```

### API documentation is unavailable

Make sure the backend server is running and check the terminal for startup errors.

Open:

```text
http://127.0.0.1:8000/docs
```

### Tests fail

Read the complete traceback and identify the failing test.

Check the environment variables, database connection, test data, and application code.

Run the failing test separately before running the complete test suite again.

## 13. Technology Stack

The backend is built using the following technologies:

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | REST API framework |
| SQLAlchemy | Object-relational mapping and database access |
| Alembic | Database migrations |
| PostgreSQL | Relational database |
| Pydantic | Data validation and serialization |
| JWT | Token-based authentication |
| unittest | Automated testing |
| GitHub Actions | Continuous Integration |

## 14. Project Structure

The backend is located in the `Backend` directory.

Important files and directories include:

| File or directory | Purpose |
|---|---|
| `main.py` | FastAPI application entry point |
| `requirements.txt` | Main Python dependencies |
| `alembic.ini` | Alembic configuration |
| `alembic/` | Database migration configuration and versions |
| `tests/` | Automated tests |
| `tests/unit/` | Unit tests |
| `tests/api/` | API tests |
| `tests/integration/` | Integration tests |
| `.venv/` | Local Python virtual environment |

The application also contains modules for API controllers, models, services, DTOs, and other backend functionality.

To inspect the complete directory structure, run this command from the `Backend` directory:

```powershell
tree /F
```

## 15. Useful Commands Reference

All commands below assume that the terminal is opened in the `Backend` directory.

| Task | Command |
|---|---|
| Create virtual environment | `python -m venv .venv` |
| Activate virtual environment | `.\.venv\Scripts\Activate.ps1` |
| Install dependencies | `python -m pip install -r requirements.txt` |
| Start backend | `.\.venv\Scripts\python.exe -m uvicorn main:app --reload` |
| Check migration | `alembic current` |
| View migration history | `alembic history` |
| Apply migrations | `alembic upgrade head` |
| Create migration | `alembic revision --autogenerate -m "description"` |
| Roll back migration | `alembic downgrade -1` |
| Run unit tests | `.\.venv\Scripts\python.exe -m unittest discover -s tests\unit -v` |
| Run API tests | `.\.venv\Scripts\python.exe -m unittest discover -s tests\api -v` |
| Run integration tests | `.\.venv\Scripts\python.exe -m unittest discover -s tests\integration -v` |
| Run all tests | `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` |

## 16. Additional Resources

- [Project GitHub Repository](https://github.com/Maxim-91/Accommodation-booking-service)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
