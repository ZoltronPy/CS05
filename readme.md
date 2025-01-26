Travel Management System
Overview
The Travel Management System is a web-based application designed to streamline the management of travel services for agencies. It offers an intuitive and efficient platform for handling tours, customers, employees, and various travel-related resources. Whether you're managing tour bookings, tracking customer inquiries, or overseeing employee assignments, this system is built to enhance organization and productivity.

Features
1. Travel Management
Tour Listings: Display available tours with detailed information, including destinations, hotels, and pricing.
Search and Filter: Quickly search for tours using filters like destination, price range, and availability.
Promotions and Discounts: Highlight last-minute deals and promotional offers.
2. Booking System
Customer Bookings: Enable customers to book tours, specifying the number of adults and children.
Real-Time Updates: Automatically adjust seat availability and update booking statuses.
3. Employee Management
Role-Based Access: Manage employees with defined roles such as Manager, Senior, and Customer Service.
Assignment Tracking: Assign tours and customer inquiries to specific employees for streamlined task delegation.
4. Customer Communication
Contact Messages: Handle customer inquiries efficiently with a built-in messaging system.
Status Updates: Track and update the status of messages, ensuring timely responses.
5. Dynamic Admin Panel
Manage destinations, countries, cities, and hotels from an intuitive admin interface.
Update and organize data without needing technical expertise.
6. Reports and Analytics
Generate reports on bookings, customer interactions, and employee performance.
Visualize data to make informed decisions.
Who is it for?
This system is ideal for travel agencies that need a comprehensive solution for managing their day-to-day operations. It simplifies tasks like booking management, customer communication, and resource allocation, saving time and reducing errors.

Key Technologies
Backend: Django (Python)
Frontend: HTML, CSS, Bootstrap
Database: SQLite (default, replaceable with other DBs like PostgreSQL or MySQL)
Other Tools: Django Admin, GeoIP2 for location-based features.
How to Use
Setup: Install the required dependencies and run the server locally.
Login: Access the admin panel or user dashboard based on your role.
Explore: Manage tours, bookings, employees, and inquiries effortlessly.
Reports: Use the reporting features to analyze and improve performance.
Installation
Prerequisites
Python 3.8 or higher
Django 4.x or higher
Virtual environment (recommended)


Clone the repository:
bash
Zkopírovat
Upravit
git clone https://github.com/ZoltronPy/CS05.git
Navigate to the project directory:
bash
Zkopírovat
Upravit
cd travel-management-system
Create and activate a virtual environment:
bash
Zkopírovat
Upravit
python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows
Install dependencies:
bash
Zkopírovat
Upravit
pip install -r requirements.txt
Apply migrations:
bash
Zkopírovat
Upravit
python manage.py migrate
Run the server:
bash
Zkopírovat
Upravit
python manage.py runserver