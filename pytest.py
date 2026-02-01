import argparse
import random
import requests
import json
import time
import string


# Configuration - change this if your backend runs on different host/port
BASE_URL = "http://127.0.0.1:8000"
HEADERS = {"Content-Type": "application/json"}

def api_post(endpoint, data=None, token=None):
    """Helper: POST request with optional token"""
    url = f"{BASE_URL}{endpoint}"
    headers = HEADERS.copy()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        print("url:",url)
        r = requests.post(url, json=data, headers=headers, timeout=8)
        return r.status_code, r.json() if r.text else {}
    except Exception as e:
        return 0, {"error": str(e)}

def api_put(endpoint, data=None, token=None):
    """Helper: PUT request with optional token"""
    url = f"{BASE_URL}{endpoint}"
    headers = HEADERS.copy()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        print("url:",url)
        r = requests.put(url, json=data, headers=headers, timeout=8)
        return r.status_code, r.json() if r.text else {}
    except Exception as e:
        return 0, {"error": str(e)}

def api_get(endpoint, token=None):
    """Helper: GET request with optional token"""
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = requests.get(url, headers=headers, timeout=8)
        return r.status_code, r.json() if r.text else {}
    except Exception as e:
        return 0, {"error": str(e)}

def random_string(length=8):
    """Generate a random string of letters and digits."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
def random_fullname():
    """Generate a random full name."""
    first_names = ["John", "Jane", "Alex", "Emily", "Chris", "Anna", "Michael", "Sophia"]
    last_names = ["Smith", "Doe", "Brown", "Johnson", "Lee", "Taylor", "Wilson", "Clark"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_phone():
    """Generate a random phone number in New Zealand format."""
    # NZ mobile numbers start with 02X or 021/022/027/029 etc.
    prefixes = ["021", "022", "027", "029"]
    return f"{random.choice(prefixes)}{random.randint(1000000, 9999999)}"


def run_full_demo():
    """
    Run a complete end-to-end demo in sequence:
    1. Register normal user
    2. Login as normal user
    3. List available cars
    4. Create a booking
    5. Login as admin
    6. Approve the booking
    7. Pay for the booking
    8. Return the car
    """
    print("=== Car Rental Full Flow Demo ===\n")

    

    # Generate random username and email
    username = f"user_{random_string(6)}"
    email = f"{random_string(6)}@example.com"
    password = "password123"  # Keep password fixed for testing
    fullname = random_fullname()
    phone = random_phone()

    # Example API POST call
    status, resp = api_post("/user/", {
        "username": username,
        "password": password,
        "email": email,
        "full_name": fullname,
        "phone": phone
    })
    # ── Step 1: Register a regular user ──
    print("1. Register user 'john_doe'")
    status, resp = api_post("/user/", {
        "username": "john_doe",
        "password": "password123",
        "email": "john@example.com"
    })
    print("   →", resp.get("message", resp))


    # ── Step 2: Login as regular user ──
    print("\n2. Login as john_doe")

    resp = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={   
            "username": "john@example.com",
            "password": "password123"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if resp.status_code != 200:
        print("   Login failed!", resp.json())
        return

    data = resp.json()
    user_token = data.get("access_token")
    print("   → Login OK. Token received.Token:",user_token)

    print("\n3. Create user profile")
    status, resp = api_post(
        "/user_profile/",
        data={
            "address": "123 Queen Street",
            "city": "Auckland",
            "country": "New Zealand",
            "emergency_contact_name": "Jane Doe",
            "emergency_contact_phone": "021123456"
        },
        token=user_token
    )

    if status != 200:
        print("   Create profile failed!", resp)
        return

    print("   → User profile created")



    print("\n4. Create driver license")

    status, resp = api_post(
        "/driver_license/",
        data={
            "license_number": "NZDL1234567",
            "license_pic": "mock_license.jpg",
            "expire_date": "2030-12-31"
        },
        token=user_token
    )

    if status != 200:
        print("   Create driver license failed!", resp)
        return

    print("   → Driver license created")

    # ── Step 3: List available cars ──
    print("\n3. List available cars")
    status, cars = api_get("/car", user_token)
    if status != 200 or not isinstance(cars, list):
        print("   Failed to get cars", cars)
        return

    if not cars:
        print("   No cars available in the system!")
        return

    car = cars[0]  # take first car
    car_id = car.get("car_id")
    print(f"   → Found {len(cars)} cars. Using car ID = {car_id}")

    # ── Step 4: Create a booking ──
    print("\n4. Create booking (3 days from today)")
    start_date = "2026-04-10"
    end_date   = "2026-04-13"

    status, booking = api_post("/booking/", {
        "car_id": car_id,
        "start_date": start_date,
        "end_date": end_date,
        "insurance_price_id":2
    }, user_token)

    if status not in (200, 201):
        print("   Booking failed!", booking)
        return

    booking_id = booking.get("id") or booking.get("booking_id")
    print(f"   → Booking created! ID = {booking_id}")


    print("6. Login as admin")

    resp = requests.post(
            f"{BASE_URL}/api/auth/login",
            data={   
               "username": "admin@gmail.com",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
    
    if resp.status_code != 200:
        print("   Login failed!", resp.json())
        return

    data = resp.json()
    user_token = data.get("access_token")
    print("   → Login OK. Token received.Token:",user_token)

    admin_token = resp.json().get("access_token")
    print("   → Admin login OK.admin_token:",admin_token)

    # ── Step 7: Admin approves the booking ──
    print(f"\n7. Admin approves booking #{booking_id}")
    status, result = api_put(f"/booking/approval/{booking_id}",data={"status": 1}, token=admin_token)
    print("   →", result.get("message", result))

    # Small delay to simulate real-world timing
    time.sleep(1.2)

    # ── Step 8: User pays for the booking ──
    print(f"\n8. User pays for booking #{booking_id}")
    # In real system you'd get the real amount from /api/bookings/{id}
    amount = 299.0
    status, payment = api_post("/payment/", {
        "booking_id": booking_id,
        "amount": amount
    }, user_token)
    print("   →", payment)

    # ── Step 9: User returns the car ──
    print(f"\n9. User returns car (completes booking #{booking_id})")
    status, result = api_put(f"/booking/return/{booking_id}",
                             data={
                            "booking_id": booking_id,
                            "end_date": "2026-04-13T05:55:28.022Z",
                            "drop_location": 0
                            },
                            token=user_token)
    print("   →", result.get("message", result))

    print("\n=== Demo completed ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Car Rental CLI Client")
    parser.add_argument("--demo", action="store_true",
                        help="Run full end-to-end demo sequence")

    # You can keep other commands if needed...
    subparsers = parser.add_subparsers(dest="command")
    # ... (register, login, book, approve, pay, return_car, etc.)

    args = parser.parse_args()

    if args.demo:
        run_full_demo()
    else:
        print("Use --demo to run the complete flow")
        parser.print_help()