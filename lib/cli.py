from helpers import (
    exit_program,
    list_users, find_user_by_email, find_user_by_id, create_user, update_user, delete_user,
    list_turfs, find_turf_by_name, find_turf_by_id, create_turf, update_turf, delete_turf,
    list_turf_slots, find_turf_slot_by_id, create_turf_slot, update_turf_slot, delete_turf_slot,
    list_bookings, find_booking_by_id, create_booking, update_booking, delete_booking
)

def main_menu():
    while True:
        print("\n=== Turf Time Management System ===")
        print("1. Manage Users")
        print("2. Manage Turfs")
        print("3. Manage Turf Slots")
        print("4. Manage Bookings")
        print("5. Exit")
        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            users_menu()
        elif choice == "2":
            turfs_menu()
        elif choice == "3":
            turf_slots_menu()
        elif choice == "4":
            bookings_menu()
        elif choice == "5":
            exit_program()
        else:
            print("Invalid choice. Please try again.")

def users_menu():
    while True:
        print("\n--- Users Menu ---")
        print("1. List all users")
        print("2. Find user by email")
        print("3. Find user by id")
        print("4. Create user")
        print("5. Update user")
        print("6. Delete user")
        print("7. Back to main menu")
        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            list_users()
        elif choice == "2":
            find_user_by_email()
        elif choice == "3":
            find_user_by_id()
        elif choice == "4":
            create_user()
        elif choice == "5":
            update_user()
        elif choice == "6":
            delete_user()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

def turfs_menu():
    while True:
        print("\n--- Turfs Menu ---")
        print("1. List all turfs")
        print("2. Find turf by name")
        print("3. Find turf by id")
        print("4. Create turf")
        print("5. Update turf")
        print("6. Delete turf")
        print("7. Back to main menu")
        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            list_turfs()
        elif choice == "2":
            find_turf_by_name()
        elif choice == "3":
            find_turf_by_id()
        elif choice == "4":
            create_turf()
        elif choice == "5":
            update_turf()
        elif choice == "6":
            delete_turf()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

def turf_slots_menu():
    while True:
        print("\n--- Turf Slots Menu ---")
        print("1. List all turf slots")
        print("2. Find turf slot by id")
        print("3. Create turf slot")
        print("4. Update turf slot")
        print("5. Delete turf slot")
        print("6. Back to main menu")
        choice = input("Select an option (1-6): ").strip()
        if choice == "1":
            list_turf_slots()
        elif choice == "2":
            find_turf_slot_by_id()
        elif choice == "3":
            create_turf_slot()
        elif choice == "4":
            update_turf_slot()
        elif choice == "5":
            delete_turf_slot()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def bookings_menu():
    while True:
        print("\n--- Bookings Menu ---")
        print("1. List all bookings")
        print("2. Find booking by id")
        print("3. Create booking")
        print("4. Update booking")
        print("5. Delete booking")
        print("6. Back to main menu")
        choice = input("Select an option (1-6): ").strip()
        if choice == "1":
            list_bookings()
        elif choice == "2":
            find_booking_by_id()
        elif choice == "3":
            create_booking()
        elif choice == "4":
            update_booking()
        elif choice == "5":
            delete_booking()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    main_menu()

if __name__ == "__main__":
    main()
