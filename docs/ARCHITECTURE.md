# Architecture Overview

The recipe community platform is designed as a modular monorepo with dedicated workspaces for front-end applications, backend services, and reusable libraries. The initial milestone focuses on the public API service, laying the foundation for future web and mobile clients, asynchronous workers, and recommendation engines.

## Services

### API (FastAPI)

- **Purpose**: Expose RESTful endpoints for recipe discovery, ingredient management, and meal planning.
- **Tech stack**: FastAPI, SQLAlchemy 2.0, Pydantic v2, PostgreSQL (SQLite for local development).
- **Key modules**:
  - `app/core`: configuration and helper utilities.
  - `app/models`: SQLAlchemy models representing recipes, ingredients, and associations.
  - `app/schemas`: Pydantic models for request/response validation.
  - `app/crud`: persistence logic separated from the API layer.
  - `app/api`: versioned routers and dependencies for FastAPI.

### Web (apps/web)

Placeholder for the future React/Next.js client. It will consume the API service and introduce client-side rendering, server-side rendering, and caching strategies tailored for recipe discovery and community features.

## Data Layer

- Normalized relational schema with join tables for many-to-many relationships (recipes ↔ ingredients).
- Database session management via dependency injection ensuring scoped sessions per request.
- Automatic table creation on startup for development convenience (to be replaced with migrations in production).

## Testing Strategy

- Service-level tests live under `services/api/tests` and exercise API endpoints via the FastAPI TestClient.
- Fixtures provide an in-memory SQLite database for deterministic, isolated test runs.

## Roadmap

1. **Authentication & Authorization**: Introduce user accounts, OAuth providers, and role-based access.
2. **Content Enrichment**: Extend models with media assets, dietary tags, and structured preparation steps.
3. **Community Modules**: Implement posts, comments, likes, and curated collections.
4. **Recommendation Engine**: Combine collaborative filtering and rule-based dietary preferences.
5. **Operational Tooling**: Add observability (metrics, tracing), CI/CD pipelines, and deployment manifests.
