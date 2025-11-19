# Docker Deployment Guide

This guide explains how to run the ADK application, mock Ollama server, and PostgreSQL database using Docker.

## Architecture

The Docker setup consists of three services:

1. **postgres** - PostgreSQL database for session storage
2. **ollama-mock** - Mock Ollama server for testing
3. **adk-app** - Your Google ADK application

All services are connected via a Docker network and can communicate with each other.

## Prerequisites

- Docker installed (version 20.10 or higher)
- Docker Compose installed (version 2.0 or higher)

## Quick Start

### 1. Configure Environment Variables

Copy the example environment file:

```powershell
Copy-Item .env.docker .env
```

Edit `.env` and set your values:

```env
DB_HOST=postgres
DB_USER=adk_user
DB_PASSWORD=adk_password
OLLAMA_API_BASE=http://ollama-mock:11434
```

### 2. Build and Start All Services

```powershell
docker-compose up --build
```

Or run in detached mode:

```powershell
docker-compose up -d --build
```

### 3. Access the Services

- **ADK App**: http://localhost:8000
- **Mock Ollama Server**: http://localhost:11434
- **PostgreSQL**: localhost:5432

### 4. View Logs

```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f adk-app
docker-compose logs -f ollama-mock
docker-compose logs -f postgres
```

### 5. Stop Services

```powershell
docker-compose down
```

To also remove volumes (database data):

```powershell
docker-compose down -v
```

## Service Details

### PostgreSQL Database

- **Container Name**: adk-postgres
- **Port**: 5432
- **Database**: mydatabase
- **User**: Configured via `DB_USER` env variable
- **Password**: Configured via `DB_PASSWORD` env variable
- **Data Persistence**: Volume `postgres_data` (survives container restarts)

### Mock Ollama Server

- **Container Name**: ollama-mock-server
- **Port**: 11434
- **Health Check**: Checks if server is responding on root endpoint
- **Purpose**: Simulates Ollama API for testing without requiring actual Ollama

### ADK Application

- **Container Name**: adk-app
- **Port**: 8000
- **Dependencies**: Waits for PostgreSQL to be healthy before starting
- **Hot Reload**: The `src` directory is mounted as a volume for development

## Development Workflow

### Making Changes to Your Agent

Since the `src` directory is mounted as a volume, changes to your agents will be reflected in the container. However, you may need to restart the ADK app:

```powershell
docker-compose restart adk-app
```

### Rebuilding After Dependency Changes

If you modify `requirements.txt`:

```powershell
docker-compose up -d --build adk-app
```

### Accessing PostgreSQL

Connect to the database:

```powershell
docker exec -it adk-postgres psql -U adk_user -d mydatabase
```

Or use a database client with:
- Host: localhost
- Port: 5432
- Database: mydatabase
- User: adk_user (or your configured user)
- Password: adk_password (or your configured password)

## Troubleshooting

### Port Already in Use

If you get "port already in use" errors, modify the port mappings in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Change 8001 to any available port
```

### Database Connection Issues

Check if PostgreSQL is healthy:

```powershell
docker-compose ps
```

View PostgreSQL logs:

```powershell
docker-compose logs postgres
```

### Mock Ollama Not Responding

Verify the mock server is running:

```powershell
curl http://localhost:11434/
```

Check logs:

```powershell
docker-compose logs ollama-mock
```

### ADK App Not Starting

Check dependencies are running:

```powershell
docker-compose ps
```

View app logs:

```powershell
docker-compose logs adk-app
```

## Production Considerations

For production deployment, consider:

1. **Use secrets management** instead of environment variables in `.env`
2. **Configure proper PostgreSQL backup** strategy
3. **Set up reverse proxy** (nginx/traefik) for SSL/TLS
4. **Adjust resource limits** in docker-compose.yml
5. **Use Docker secrets** for sensitive data
6. **Enable PostgreSQL authentication** with stronger passwords
7. **Consider using managed database** services

## Customization

### Changing PostgreSQL Version

Edit `docker-compose.yml`:

```yaml
postgres:
  image: postgres:16-alpine  # Change version
```

### Adding More Mock Server Responses

Edit `ollama_mock_server/server.py` and rebuild:

```powershell
docker-compose up -d --build ollama-mock
```

### Scaling Services

Run multiple instances of the ADK app:

```powershell
docker-compose up -d --scale adk-app=3
```

Note: You'll need to configure a load balancer for this to work properly.

## Useful Commands

```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart a specific service
docker-compose restart adk-app

# View running containers
docker-compose ps

# Execute command in container
docker-compose exec adk-app python -c "print('Hello')"

# Remove all containers, networks, and volumes
docker-compose down -v

# Pull latest images
docker-compose pull

# Build without cache
docker-compose build --no-cache
```
