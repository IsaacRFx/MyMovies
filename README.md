# My Movies Project

## Team
Edwin Isaac Rodriguez Flores - 19211721
Miguel Adrián Hernández Vázquez - 19211657

## Project video

https://www.youtube.com/watch?v=uvvEjtvUVqQ

## Features

* User system
  1. Sign-up
  2. Login
* Movie catalog
* Movie details
* Movie reviews
* Movie recommendations
* Actor catalog
* Actor details
* Load scripts
  1. Genres
  2. Movies
* Dockerized project
* Deployment
  1. Deployed on a container on EC2 instance, accessable through [custom dns](gutelekture.ddns.net:8000/) (when EC2 instance is active)
  2. Using RDS database (Postgres)

## Example .env (in case you want to run this project)

```
TMDB_READ_ACCESS_TOKEN='<YOUR-TMDB-ACCESS-TOKEN>'
TMDB_API_BASE_URL='https://api.themoviedb.org/3'
ENVIRONMENT=True|False (DEBUG|PROD)
ALLOWED_HOSTS='localhost'
```
