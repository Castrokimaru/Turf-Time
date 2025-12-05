from .db.models import User, Booking

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
