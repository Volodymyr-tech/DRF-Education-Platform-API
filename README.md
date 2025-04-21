# DRF Education Platform

This is an educational platform backend built with Django REST Framework. It provides core features for managing users, courses, and materials.

## Features

- User registration and authentication (JWT-based)  
- Role‑based permissions (Admin, Moders, User)  
- Course management (create, update, delete)  
- Adding learning materials to courses  
- API documentation (Swagger / ReDoc)  
- Filtering, pagination, and search  
- Stripe integration for payments  
- Asynchronous tasks with Celery & Redis  

## Tech Stack

- **Python** 3.11  
- **Django** 5.1  
- **Django REST Framework**  
- **PostgreSQL** 17  
- **Redis** 7  
- **Celery** (with eventlet)  
- **Swagger** (drf‑yasg)  
- **Stripe** payments  
- **Poetry** for dependency management  
- **Docker** & **Docker Compose**  

## Prerequisites

- Docker (Engine & CLI)  
- Docker Compose (v3.9)  
- A valid `.env` file at project root  

## Environment Variables
### This project uses two separate environment files:
- **`.env`** — contains all variables needed for local development (dev).  
- **`.env.docker`** — contains only the variables required by the containers when running via Docker Compose.


#### .env 
- SECRET_KEY=
- NAME=
- USER=
- PASSWORD=
- HOST=
- PORT=
- STRIPE_API_KEY=
- EMAIL_HOST=
- EMAIL_PORT=
- EMAIL_USE_SSL=
- EMAIL_HOST_USER=
- EMAIL_HOST_PASSWORD=
- CELERY_BROKER_URL='redis://localhost:6379/0'
- CELERY_RESULT_BACKEND='redis://localhost:6379/0'

#### .env.docker
- POSTGRES_HOST=
- POSTGRES_PORT=
- POSTGRES_USER=
- POSTGRES_PASSWORD=
- POSTGRES_DB=

- CELERY_BROKER_URL='redis://redis:6379/0'
- CELERY_RESULT_BACKEND='redis://redis:6379/0'


## Running with Docker

### Build & start all services
- docker-compose up -d --build

### Services

- web (Django + Gunicorn, port 8000)
- db (PostgreSQL 17)
- redis (Redis 7)
- celery (Celery worker)
- celery_beat (Celery beat scheduler)

The web service will automatically apply migrations, collect static files, and launch Gunicorn.

## Access the platform

- API root & Swagger: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- Admin panel: http://localhost:8000/admin/

## Running Locally (without Docker)

#### Install dependencies:
- poetry install

#### Configure .env as above.

#### Apply migrations & start dev server:
- python manage.py migrate
- python manage.py runserver

#### Testing & Coverage
- coverage run --source='.' manage.py test
- coverage report

## Project Structure
- config/           Django project settings & WSGI entrypoint
- materials/        Materials app (models, views, serializers)
- users/            Users app (registration, auth, permissions)
- manage.py         Django CLI utility
- pyproject.toml    Project metadata & dependencies
- poetry.lock       Locked dependency graph
- Dockerfile        Docker image definition
- docker-compose.yml   Multi‐container orchestration
- .env, .env.docker     Environment configuration


### Author: Valdemar — vovateslenko.1996.28@gmail.com