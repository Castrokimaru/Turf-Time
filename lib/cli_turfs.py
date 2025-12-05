from .db.models import Turf, TurfSlot, Booking

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
