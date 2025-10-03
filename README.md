# Recipe Community Platform

A modern reimagining of the original desktop nutrition planner, rebuilt as a service-oriented web platform for recipe discovery, meal planning, and community engagement.

## Monorepo Layout

```
recipe-diet/
├── apps/
│   └── web/                  # Future web client (Next.js / React)
├── services/
│   └── api/                  # FastAPI backend service
├── libs/                     # Reusable shared libraries
├── docs/                     # Product & architecture documentation
├── deploy/                   # Deployment tooling and infrastructure assets
└── tests/                    # Cross-service integration tests (future)
```

This commit bootstraps the backend API service and common documentation while leaving room for the web and worker applications that will follow.

## Backend Service

The API is implemented with [FastAPI](https://fastapi.tiangolo.com/) and SQLAlchemy. It exposes REST endpoints to manage recipes, ingredients, and their relationships. Highlights include:

- SQL modeling for recipes, ingredients, and join table with timestamps
- Dependency-injected SQLAlchemy sessions with environment-driven configuration
- Clean separation of models, schemas, CRUD logic, and routers
- Comprehensive JSON schemas for request/response payloads
- Automated database initialization on application startup

### Local Development

1. **Install dependencies**

   ```bash
   pip install -r services/api/requirements.txt
   ```

2. **Run the API**

   ```bash
   uvicorn app.main:app --reload --factory --app-dir services/api
   ```

3. **Interactive Docs**

   Visit `http://127.0.0.1:8000/docs` for the auto-generated Swagger UI.

### Running Tests

```bash
pytest
```

Pytest discovers the service-level tests located in `services/api/tests/`.

## Next Steps

- Implement authentication & user profiles
- Expand recipe metadata (media assets, dietary tags)
- Introduce recommendation, feed, and social modules
- Scaffold the web front-end client under `apps/web`
- Add CI/CD pipeline definitions and deployment manifests under `deploy/`

