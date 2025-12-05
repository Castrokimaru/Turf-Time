from .db.models import Booking
import datetime

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
