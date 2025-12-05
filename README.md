# Turf-Time

A Python CLI application for managing turf time bookings using Object-Relational Mapping (ORM) with SQLAlchemy.

## Features

- **User Management**: Create, view, and manage user accounts with roles (player/admin).
- **Turf Management**: Add and manage turf locations with pricing and availability.
- **Slot Management**: Define time slots for turfs with pricing and status.
- **Booking System**: Book slots for users, track bookings, and manage statuses.
- **CLI Interface**: Interactive command-line interface with menus for all operations.
- **Data Validation**: Built-in validation for all inputs and relationships.

## Database Schema

- **Users**: id, email, password_hash, role, city
- **Turfs**: id, name, city, latitude, longitude, base_price_per_hour, is_active
- **Turf Slots**: id, turf_id, slot_date, start_time, end_time, status, final_price
- **Bookings**: id, turf_id, slot_id, user_id, booking_date, total_amount, status

Relationships:
- Turf has many Slots and Bookings
- User has many Bookings
- Slot has many Bookings

## Installation

1. Install dependencies:
   ```bash
   pipenv install
   ```

2. Activate virtual environment:
   ```bash
   pipenv shell
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Usage

The application provides a menu-driven CLI. Navigate through the menus to:
- Manage users, turfs, slots, and bookings
- Create new records
- View and search existing data
- Delete records

## Seeding

To populate the database with sample data:
```bash
python lib/db/seed.py
```

## Requirements

- Python 3.10+
- SQLAlchemy
- Click (for CLI enhancements, though core CLI is built-in)