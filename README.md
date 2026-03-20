# Travel Planner

A CRUD application to manage travel projects and places, built with Django, Django REST Framework, and SQLite.

## Features
- Manage travel projects (create, read, update, delete).
- A project can optionally be created with up to 10 places in a single request.
- Add, update, and remove places within a travel project.
- Notes can be added to places and they can be marked as visited.
- When all places in a project are marked as visited, the project is automatically marked as completed.
- Third-party API integration: Places are validated against the [Art Institute of Chicago API](https://api.artic.edu/docs/#collections).

## Requirements
- Python 3.14 (or use provided Docker configuration)
- [uv](https://github.com/astral-sh/uv) (for local setup) or Docker with Docker Compose.

## How to build and run

### Using Docker (Recommended)
You can start the application quickly using Docker:

```bash
make up
# or
docker compose up -d
```

The server will be available at `http://localhost:8000/`.

To run tests inside Docker:
```bash
docker compose run --rm web uv run python manage.py test
```

### Local Setup
1. Copy the example environment variables:
   ```bash
   make env
   ```
2. Install dependencies, run migrations using `uv`:
   ```bash
   make setup
   ```
3. Start the application:
   ```bash
   make run
   ```

To run tests locally:
```bash
make test
```

To create an admin superuser:
```bash
make superuser
```

## API Documentation
The API is fully documented using OpenAPI schema. Once the app is running, you can access:
- **Swagger UI**: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
- **Redoc**: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)
- **Raw Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

## Example Requests

### Create a travel project with places
```bash
curl -X POST http://localhost:8000/api/travel-projects/ \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Chicago Trip",
           "description": "Visiting museums",
           "start_date": "2026-04-01",
           "places": [
             {
               "external_id": "129884",
               "notes": "Starry Night is a must see",
               "is_visited": false
             }
           ]
         }'
```

*(Note: "129884" is an example valid ID from the Art Institute API. If you try to pass an invalid ID, the request will fail.)*

### Add a place to an existing project
```bash
curl -X POST http://localhost:8000/api/travel-projects/1/places/ \
     -H "Content-Type: application/json" \
     -d '{
           "external_id": "27992",
           "notes": "American Gothic"
         }'
```
