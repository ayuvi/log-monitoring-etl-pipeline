import time
import random
from datetime import datetime

services = [
    "auth-service",
    "payment-service",
    "booking-service",
    "notification-service",
    "database-service"
]

levels = ["INFO", "INFO", "INFO", "WARN", "ERROR"]  # error lebih jarang

messages = {
    "auth-service": [
        "User login success user_id={}",
        "User logout user_id={}",
        "Invalid password user_id={}"
    ],
    "payment-service": [
        "Payment success order_id={}",
        "Payment gateway timeout order_id={}",
        "Refund processed order_id={}"
    ],
    "booking-service": [
        "Container booked container_id=CXRU{}",
        "Retry booking container_id=CXRU{}",
        "Booking cancelled container_id=CXRU{}"
    ],
    "notification-service": [
        "Email sent to user_id={}",
        "Push notification failed user_id={}"
    ],
    "database-service": [
        "Connection pool exhausted",
        "Slow query detected",
        "Deadlock detected"
    ]
}


def generate_log():
    service = random.choice(services)
    level = random.choice(levels)

    msg_template = random.choice(messages[service])
    number = random.randint(100, 99999)

    if "{}" in msg_template:
        message = msg_template.format(number)
    else:
        message = msg_template

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"{timestamp} {level} {service} {message}\n"


def main():
    print("Starting log generator...")
    while True:
        with open("data/app.log", "a") as f:
            f.write(generate_log())

        time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    main()
