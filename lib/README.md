# Turf Time - CLI and ORM Application

A command-line interface (CLI) application for managing turf bookings using SQLAlchemy ORM.

## Setup

1. Install dependencies:
   ```
   pipenv install
   ```

2. Enter the virtual environment:
   ```
   pipenv shell
   ```

3. Seed the database with sample data:
   ```
   python lib/seed.py
   ```

4. Run the CLI:
   ```
   python lib/cli.py
   ```

## Features

- Manage users (players and admins)
- Manage turfs with location and pricing
- Manage turf slots with availability
- Manage bookings with status tracking

## Database Schema

- Users: id, email, password_hash, role, city
- Turfs: id, name, city, latitude, longitude, base_price_per_hour, is_active
- Turf Slots: id, turf_id, slot_date, start_time, end_time, status, final_price
- Bookings: id, turf_id, slot_id, user_id, booking_date, total_amount, status

## Usage

Use the menu in the CLI to perform CRUD operations on each entity.
