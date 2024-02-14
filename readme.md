# Hotel Booking Python/Django CRU

## Description

Este proyecto es una API de gestión hotelera utilizando Django Rest Framework (DRF) y PostgreSQL. El objetivo es aprender a crear API con Django y el alcance incluye la gestión de habitaciones, huespedes, reservas y reservas de habitacion y pago por el hospedaje.

## Modelo de la db

![1707907551117](image/readme/hotelApi.png)

## Postman test

En el siguiente documento de Postman, encontrarás una explicación detallada de cada endpoint, incluyendo el propósito y la funcionalidad específica que desempeñan en el sistema. Además, se proporcionarán ejemplos y casos de uso relevantes para cada endpoint, con el fin de facilitar su comprensión y uso adecuado:

[Documento de pruevas postman](https://documenter.getpostman.com/view/1064965/2sA2r54RSN)

## Installation

Clone repository:

```
> clone ...
```

Iniciar los contenedores Docker utilizando el comando:

```
docker compose up
```

## Configure the App

Acceder al contenedor Docker con nombre 'web':

```
docker exec -it web bash
```

Run the following commands in the Docker container 'web' shell (bash) to configure:

```
> python ./manage.py makemigrations
> python ./manage.py makemigrations core
> python ./manage.py migrate
> python ./manage.py createsuperuser

```

## And navigate to Hotel API address:

```
http://localhost:8000/api/
```
