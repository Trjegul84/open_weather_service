import time

import requests

# Script to test GET endpoint in a terminal:

user_id = input("Please enter the user_id: ").strip()

for i in range(1, 25):
    print(f"Get request #{i}:\n")
    result = requests.get(f"http://localhost:8000/weather/{user_id}")
    if result.status_code != 200:
        print(f"There is a problem with the request. Status code:{result.status_code}")
        break
    print(f"Porcentaje: {result.text} \t\t Status Code: {result.status_code} \n")
    time.sleep(3)
