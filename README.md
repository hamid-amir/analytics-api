# Analytics API

In this project, I'm working on a FastAPI-based analytics API for tracking and managing events with time-series data storage using TimescaleDB.

This is mainly an educational project for myself to learn more about:

- RESTful API for event management (CRUD operations)
- Time-series database powered by TimescaleDB (PostgreSQL extension)
- Automatic data partitioning and retention policies
- FastAPI with async support
- Docker containerization for easy deployment

## Tech Stack

- **Framework**: FastAPI
- **Database**: TimescaleDB (PostgreSQL 17)
- **ORM**: SQLModel
- **Package Manager**: uv
- **Server**: Gunicorn with Uvicorn workers

## Quick Start with Docker

### 1. Create Environment File

Create a `.env.compose` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://<db-username>:<db-password>@db_service:5432/timescaledb
DB_TIMEZONE=UTC
```

### 2. Build and Run with Docker Compose

```bash
# Build and start all services
docker compose up --build

# Run with showing the online container logs
docker compose up --build -w
```

The API will be available at `http://localhost:8000`

### 3. Using Docker Commands Directly

#### Build the Docker image:

```bash
docker build -t analytics-api:v1 .
```

#### Run the database container:

```bash
docker run -d \
  --name timescaledb \
  -e POSTGRES_USER=<db-username> \
  -e POSTGRES_PASSWORD=<db-password> \
  -e POSTGRES_DB=timescaledb \
  -p 5432:5432 \
  -v timescaledb-data:/var/lib/postgresql/data \
  timescale/timescaledb:latest-pg17
```

#### Run the API container:

```bash
docker run -d \
  --name analytics-api \
  --link timescaledb:db_service \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://<db-username>:<db-password>@db_service:5432/timescaledb \
  -e DB_TIMEZONE=UTC \
  analytics-api:v1
```

## API Endpoints

- `GET /` - Health check endpoint
- `GET /healthz` - API health status
- `GET /api/events` - List events (returns latest 10)
- `GET /api/events/{event_id}` - Get event by ID
- `POST /api/events` - Create a new event
- `PUT /api/events/{event_id}` - Update an event
- `DELETE /api/events/{event_id}` - Delete an event

## API Documentation

Once the service is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Configuration

The application uses TimescaleDB with the following default settings:
- **Chunk interval**: 1 day
- **Data retention**: 3 months (automatic cleanup)

## Development

The Docker Compose setup includes hot-reload support. Changes to source files in `./src` will automatically reload the server.

## Project Structure

```
analytics-api/
├── src/
│   ├── main.py              # FastAPI application entry point
│   └── api/
│       ├── db/              # Database configuration and session management
│       └── events/          # Event models and routing
├── boot/
│   └── docker-run.sh        # Container startup script
├── Dockerfile               # Docker image definition
├── compose.yaml             # Docker Compose configuration
└── pyproject.toml           # Python dependencies
```

## Stopping Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes (clears database data)
docker compose down -v
```
