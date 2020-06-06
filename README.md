# Example fastapi mongodb app

## Backend Requirements

* Docker
* Docker Compose
* poetry

## Backend local development

root directory is `./app` run all command from this dir.

### General workflow

Open your editor at `./app/` (instead of the project root: `./`), so that you see an `./app/` directory with your code inside. That way, your editor will be able to find all the imports, etc.

Modify or add SQLAlchemy models in `./app/app/models/`, Pydantic schemas in `./app/app/schemas/`, API endpoints in `./app/app/api/`, CRUD (Create, Read, Update, Delete) utils in `./app/app/crud/`. The easiest might be to copy the ones for Items (models, endpoints, and CRUD utils) and update them to your needs.

Add and modify tasks to the Celery worker in `./app/app/worker.py`. 

If you need to install any additional package to the worker, add it to the file `./app/celeryworker.dockerfile`.

There is an `.env` file that has some Docker Compose and app default values that allow you to just run `docker-compose up -d` and start working, while still being able to use and share the same Docker Compose files for deployment, avoiding repetition of code and configuration as much as possible.

Use `.env` file  for local development:

```bash
export $(grep -v '^#' .env | xargs -0)
```
or

```bash
source .env
```

or
 
```bash
. .env
```

### Docker Compose start source services

Start database and queue for celary:

```bash
docker-compose up -d
```

### Start App

You can run that app with:

```bash
python app/main.py
```

...it will look like:

and then hit enter. That runs the live reloading server that auto reloads when it detects code changes.

Nevertheless, if it doesn't detect a change but a syntax error, it will just stop with an error. But as the container is still alive and you are in a Bash session, you can quickly restart it after fixing the error, running the same command ("up arrow" and "Enter").

### App endpoins

* Backend, JSON based web API based on OpenAPI: http://0.0.0.0:8000/api/

* Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://0.0.0.0:8000/docs

* Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://0.0.0.0:8000/redoc


### Backend tests

To test the backend run:

```bash
sh ./scripts/test.sh
```

The tests run with Pytest, modify and add tests to `./app/app/tests/`.
