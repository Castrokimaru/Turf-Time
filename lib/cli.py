from .db.models import Session, User, Turf, TurfSlot, Booking
import datetime

def create_user(session):
    try:
        email = input("Email: ").strip()
        password_hash = input("Password hash: ").strip()
        role = input("Role (player/admin) [player]: ").strip() or 'player'
        city = input("City: ").strip()
        user = User.create(session, email=email, password_hash=password_hash, role=role, city=city)
        print(f"User created with ID: {user.id}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def display_all_users(session):
    users = User.get_all(session)
    if not users:
        print("No users found.")
        return
    for u in users:
        print(f"ID: {u.id}, Email: {u.email}, Role: {u.role}, City: {u.city}")

def view_user_bookings(session, user_id):
    user = User.find_by_id(session, user_id)
    if not user:
        print("User not found.")
        return
    bookings = Booking.find_by_user_id(session, user_id)
    if not bookings:
        print("No bookings found for this user.")
        return
    for b in bookings:
        print(f"Booking ID: {b.id}, Turf: {b.turf.name}, Slot Date: {b.slot.slot_date}, Amount: {b.total_amount}, Status: {b.status}")

def find_user_by_email(session):
    email = input("Email: ").strip()
    user = User.find_by_email(session, email)
    if user:
        print(f"ID: {user.id}, Email: {user.email}, Role: {user.role}, City: {user.city}")
    else:
        print("User not found.")

def user_menu(session):
    while True:
        print("\n--- User Menu ---")
        print("1. Create User")
        print("2. Delete User")
        print("3. Display All Users")
        print("4. View User's Bookings")
        print("5. Find User by Email")
        print("6. Back to Main Menu")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            create_user(session)
        elif choice == '2':
            user_id = input("User ID: ").strip()
            if User.delete(session, user_id):
                print("User deleted.")
            else:
                print("User not found.")
        elif choice == '3':
            display_all_users(session)
        elif choice == '4':
            user_id = input("User ID: ").strip()
            view_user_bookings(session, user_id)
        elif choice == '5':
            find_user_by_email(session)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

def create_turf(session):
    try:
        name = input("Name: ").strip()
        city = input("City: ").strip()
        latitude = float(input("Latitude: ").strip() or 0)
        longitude = float(input("Longitude: ").strip() or 0)
        base_price_per_hour = float(input("Base price per hour: ").strip())
        is_active = int(input("Is active (1/0) [1]: ").strip() or 1)
        turf = Turf.create(session, name=name, city=city, latitude=latitude, longitude=longitude, base_price_per_hour=base_price_per_hour, is_active=is_active)
        print(f"Turf created with ID: {turf.id}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def display_all_turfs(session):
    turfs = Turf.get_all(session)
    if not turfs:
        print("No turfs found.")
        return
    for t in turfs:
        print(f"ID: {t.id}, Name: {t.name}, City: {t.city}, Price: {t.base_price_per_hour}, Active: {t.is_active}")

def view_turf_slots(session, turf_id):
    turf = Turf.find_by_id(session, turf_id)
    if not turf:
        print("Turf not found.")
        return
    slots = TurfSlot.find_by_turf_id(session, turf_id)
    if not slots:
        print("No slots found for this turf.")
        return
    for s in slots:
        print(f"Slot ID: {s.id}, Date: {s.slot_date}, Time: {s.start_time}-{s.end_time}, Status: {s.status}, Price: {s.final_price}")

def view_turf_bookings(session, turf_id):
    turf = Turf.find_by_id(session, turf_id)
    if not turf:
        print("Turf not found.")
        return
    bookings = Booking.find_by_turf_id(session, turf_id)
    if not bookings:
        print("No bookings found for this turf.")
        return
    for b in bookings:
        print(f"Booking ID: {b.id}, User: {b.user.email}, Slot Date: {b.slot.slot_date}, Amount: {b.total_amount}, Status: {b.status}")

def find_turf_by_name(session):
    name = input("Name: ").strip()
    turfs = Turf.find_by_name(session, name)
    if not turfs:
        print("No turfs found.")
        return
    for t in turfs:
        print(f"ID: {t.id}, Name: {t.name}, City: {t.city}")

def turf_menu(session):
    while True:
        print("\n--- Turf Menu ---")
        print("1. Create Turf")
        print("2. Delete Turf")
        print("3. Display All Turfs")
        print("4. View Turf's Slots")
        print("5. View Turf's Bookings")
        print("6. Find Turf by Name")
        print("7. Back to Main Menu")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            create_turf(session)
        elif choice == '2':
            turf_id = input("Turf ID: ").strip()
            if Turf.delete(session, turf_id):
                print("Turf deleted.")
            else:
                print("Turf not found.")
        elif choice == '3':
            display_all_turfs(session)
        elif choice == '4':
            turf_id = input("Turf ID: ").strip()
            view_turf_slots(session, turf_id)
        elif choice == '5':
            turf_id = input("Turf ID: ").strip()
            view_turf_bookings(session, turf_id)
        elif choice == '6':
            find_turf_by_name(session)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

def create_turf_slot(session):
    try:
        turf_id = input("Turf ID: ").strip()
        slot_date = datetime.date.fromisoformat(input("Slot date (YYYY-MM-DD): ").strip())
        start_time = input("Start time (HH:MM): ").strip()
        end_time = input("End time (HH:MM): ").strip()
        status = input("Status (available/booked/cancelled) [available]: ").strip() or 'available'
        final_price = float(input("Final price: ").strip())
        slot = TurfSlot.create(session, turf_id=turf_id, slot_date=slot_date, start_time=start_time, end_time=end_time, status=status, final_price=final_price)
        print(f"Turf slot created with ID: {slot.id}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def display_all_turf_slots(session):
    slots = TurfSlot.get_all(session)
    if not slots:
        print("No turf slots found.")
        return
    for s in slots:
        print(f"ID: {s.id}, Turf: {s.turf.name}, Date: {s.slot_date}, Time: {s.start_time}-{s.end_time}, Status: {s.status}, Price: {s.final_price}")

def view_slot_bookings(session, slot_id):
    slot = TurfSlot.find_by_id(session, slot_id)
    if not slot:
        print("Slot not found.")
        return
    bookings = slot.bookings
    if not bookings:
        print("No bookings found for this slot.")
        return
    for b in bookings:
        print(f"Booking ID: {b.id}, User: {b.user.email}, Amount: {b.total_amount}, Status: {b.status}")

def find_slot_by_turf_id(session):
    turf_id = input("Turf ID: ").strip()
    slots = TurfSlot.find_by_turf_id(session, turf_id)
    if not slots:
        print("No slots found.")
        return
    for s in slots:
        print(f"ID: {s.id}, Date: {s.slot_date}, Time: {s.start_time}-{s.end_time}, Status: {s.status}")

def turf_slot_menu(session):
    while True:
        print("\n--- Turf Slot Menu ---")
        print("1. Create Turf Slot")
        print("2. Delete Turf Slot")
        print("3. Display All Turf Slots")
        print("4. View Slot's Bookings")
        print("5. Find Slots by Turf ID")
        print("6. Back to Main Menu")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            create_turf_slot(session)
        elif choice == '2':
            slot_id = input("Slot ID: ").strip()
            if TurfSlot.delete(session, slot_id):
                print("Turf slot deleted.")
            else:
                print("Turf slot not found.")
        elif choice == '3':
            display_all_turf_slots(session)
        elif choice == '4':
            slot_id = input("Slot ID: ").strip()
            view_slot_bookings(session, slot_id)
        elif choice == '5':
            find_slot_by_turf_id(session)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

def create_booking(session):
    try:
        turf_id = input("Turf ID: ").strip()
        slot_id = input("Slot ID: ").strip()
        user_id = input("User ID: ").strip()
        booking_date = datetime.date.fromisoformat(input("Booking date (YYYY-MM-DD): ").strip())
        total_amount = float(input("Total amount: ").strip())
        status = input("Status (pending/confirmed/cancelled) [pending]: ").strip() or 'pending'
        booking = Booking.create(session, turf_id=turf_id, slot_id=slot_id, user_id=user_id, booking_date=booking_date, total_amount=total_amount, status=status)
        print(f"Booking created with ID: {booking.id}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def display_all_bookings(session):
    bookings = Booking.get_all(session)
    if not bookings:
        print("No bookings found.")
        return
    for b in bookings:
        print(f"ID: {b.id}, Turf: {b.turf.name}, User: {b.user.email}, Slot Date: {b.slot.slot_date}, Amount: {b.total_amount}, Status: {b.status}")

def view_booking_details(session, booking_id):
    booking = Booking.find_by_id(session, booking_id)
    if not booking:
        print("Booking not found.")
        return
    print(f"ID: {booking.id}")
    print(f"Turf: {booking.turf.name} ({booking.turf.city})")
    print(f"Slot: {booking.slot.slot_date} {booking.slot.start_time}-{booking.slot.end_time}")
    print(f"User: {booking.user.email} ({booking.user.role})")
    print(f"Booking Date: {booking.booking_date}")
    print(f"Total Amount: {booking.total_amount}")
    print(f"Status: {booking.status}")

def find_booking_by_user_id(session):
    user_id = input("User ID: ").strip()
    bookings = Booking.find_by_user_id(session, user_id)
    if not bookings:
        print("No bookings found.")
        return
    for b in bookings:
        print(f"ID: {b.id}, Turf: {b.turf.name}, Slot Date: {b.slot.slot_date}, Amount: {b.total_amount}, Status: {b.status}")

def booking_menu(session):
    while True:
        print("\n--- Booking Menu ---")
        print("1. Create Booking")
        print("2. Delete Booking")
        print("3. Display All Bookings")
        print("4. View Booking Details")
        print("5. Find Bookings by User ID")
        print("6. Back to Main Menu")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            create_booking(session)
        elif choice == '2':
            booking_id = input("Booking ID: ").strip()
            if Booking.delete(session, booking_id):
                print("Booking deleted.")
            else:
                print("Booking not found.")
        elif choice == '3':
            display_all_bookings(session)
        elif choice == '4':
            booking_id = input("Booking ID: ").strip()
            view_booking_details(session, booking_id)
        elif choice == '5':
            find_booking_by_user_id(session)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    # Main entry point for the CLI application
    # Creates a database session and displays the main menu in a loop
    # until the user chooses to exit
    session = Session()
    try:
        while True:
            # Display main menu options
            print("\n=== Turf-Time CLI ===")
            print("1. Users")
            print("2. Turfs")
            print("3. Turf Slots")
            print("4. Bookings")
            print("5. Exit")
            choice = input("Choose a menu: ").strip()
            # Route to appropriate submenu based on user choice
            if choice == '1':
                user_menu(session)
            elif choice == '2':
                turf_menu(session)
            elif choice == '3':
                turf_slot_menu(session)
            elif choice == '4':
                booking_menu(session)
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    finally:
        # Ensure session is closed even if an error occurs
        session.close()

if __name__ == '__main__':
    main_menu()
