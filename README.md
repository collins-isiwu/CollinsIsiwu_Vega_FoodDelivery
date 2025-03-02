# CollinsIsiwu_Vega_FoodDelivery

# 🍔 Food Delivery System

This repository contains the backend for a food delivery system built with Django and Docker. The project is designed to manage orders, restaurants, couriers, and users, and includes various custom functionalities using Celery.

## 🛠 Tech Stack
- **Backend**: Django, Django Rest Framework
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **Task Queue**: Celery with RabbitMQ

---
## Link to Postman Collection
```
https://elements.getpostman.com/redirect?entityId=34423915-2baf39b7-3be5-4a7e-bac8-b20a56a89ece&entityType=collection
```
---

## 🚀 Getting Started

### Prerequisites
Ensure you have the following installed on your machine:
- **Docker** and **Docker Compose**
- **Python** 3.x (for any non-Docker use)

### 1. Clone the Repository
```bash
https://github.com/collins-isiwu/CollinsIsiwu_Vega_FoodDelivery.git
cd CollinsIsiwu_Vega_FoodDelivery
```

### 2. Create a .env file in the root directory
```
DATABASE_NAME=fooddelivery

DATABASE_USER=user

DATABASE_PASSWORD=password

DATABASE_HOST=db 

DATABASE_PORT=5432

SECRET_KEY=django-insecure-+)s4scl9061*4f_l$lq8$2x%c^n0ppb+py*6_qdsj+5-he^i=z

OPENCAGE_API_KEY=8a206e8037f04a4f9482deba27aacbd3 
```

### 3. Build and Run Docker Containers
``` 
docker-compose up --build 
```

This command will:
- Build the Django image
- Start up the PostgreSQL database, Django, and RabbitMQ (for Celery)


### 4. Apply Migrations
Once the containers are up, you'll need to apply migrations for Django:

``` 
docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate 
 
```

### 5. Create Superuser (Admin)
To create a superuser account, use the following command:

``` 
docker-compose exec web python manage.py createsuperuser 
```


### 6. Custom Management Commands
Populate Database
I've made it easy to test the APIs by creating commands to populate the database.
These include: restaurants, users, and food.

You can run the following commands after starting your containers:

``` 
docker-compose exec web python manage.py populate_restaurants 

docker-compose exec web python manage.py populate_users 

docker-compose exec web python manage.py populate_food 
```


### 7. Additional Information
Running Celery Worker
- To handle background tasks such as order processing, you'll need to run the Celery worker in a separate container. Use the following command:

``` 
docker-compose exec web celery -A fooddelivery worker --loglevel=info
```


### 8. Accessing the Admin Panel
Once everything is running, you can access the Django admin panel at:

``` 
http://localhost:8000/admin/ 

```

Create a Django default admin with:
``` 
docker-compose exec web python manage.py createsuperuser
```


### 9. Running Tests
To run unit tests for the project, use the following command:

``` 
docker-compose exec web python manage.py test 
```

### 10. Useful Docker Commands
Stop all containers:

``` 
docker-compose down 
```

Rebuild and restart containers:

``` 
docker-compose up --build
```

View logs:
``` 
docker-compose logs 
```