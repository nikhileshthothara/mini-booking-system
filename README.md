QuickBook - Facility Booking System

Project Overview

QuickBook is a Django-based web application that allows users to book facilities based on capacity. Users can sign up, log in, create, update, and cancel their bookings while ensuring no overlapping reservations occur.

Features

1.  User authentication (Signup, Login, Logout)
2.  Facility management (List, Check Availability)
3.  Booking management system with conflict detection (Prevent overlapping bookings) (Create, List, Update)
4.  AJAX-based form submissions for better user experience (Used JavaScript)
5.  Celery and RabbitMQ usage for notifications related to booking status
6.  Bootstrap-based UI
7.  Unit tests for critical functioanlity (Booking Management)
8.  Docker support for easy development and deployment

Tech Stack

Backend: Django, Django ORM
Frontend: HTML, CSS, Bootstrap, JavaScript (AJAX)
Database: PostgreSQL
Authentication: Django’s built-in auth system
Containerization: Docker, Docker Compose
Tasks: Celery, RabbitMQ


Installation
    - git clone git@github.com:nikhileshthothara/mini-booking-system.git
    - cd mini-booking-system/
    - docker-compose build
    - docker-compose up -d

Create a Superuser (Admin Access)
    - docker-compose exec web python manage.py createsuperuser

Access the Application
    - Navigate to localhost:8000
