**QuickBook - Facility Booking System**

**Project Overview**

QuickBook is a Django-based web application that allows users to book facilities based on capacity. Users can sign up, log in,  
create, update, and cancel their bookings while ensuring no overlapping reservations occur.

**Features**

1.  User authentication (Signup, Login, Logout)
2.  Facility management (List, Check Availability)
3.  Booking management system with conflict detection (Prevent overlapping bookings) (Create, List, Update)
4.  AJAX-based form submissions for better user experience (Used JavaScript)
5.  Celery and RabbitMQ usage for notifications related to booking status
6.  Bootstrap-based UI
7.  Unit tests for critical functioanlity (Booking Management)
8.  Docker support for easy development and deployment

**Tech Stack**

    1. Backend: Django, Django ORM
    2. Frontend: HTML, CSS, Bootstrap, JavaScript (AJAX)
    3. Database: PostgreSQL
    4. Authentication: Django’s built-in auth system
    5. Containerization: Docker, Docker Compose
    6. Tasks: Celery, RabbitMQ


**Installation**  
    1. git clone git@github.com:nikhileshthothara/mini-booking-system.git  
    2. cd mini-booking-system/  
    3. docker-compose build  
    4. docker-compose up -d  

**Create a Superuser (Admin Access)**  
    1. docker-compose exec web python manage.py createsuperuser

**Access the Application**  
    1. Navigate to localhost:8000

**Areas for Improvement**  
    1. Modify's (marked in code) can be implemented  
    2. Logging system can be added  
    3. Task Revocation (celery) for tasks can be added  
    4. Password management (Forgot, Reset)  
    5. More Interactive UI (using Modals for creation and updatation)  
    6. Use SES for Emails (currently using console)  
    7. On Production level create RabbitMQ users  
    8. Add Pagination related to Bookings and Facilities (Large scale)  
    9. Better UI for empty states (403, 400)  