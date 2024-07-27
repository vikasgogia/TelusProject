import requests
import time
import numpy as np

api_endpoint = "http://127.0.0.1:3000/send-task"
url = "http://127.0.0.1:3000/record"
headers = {'Content-Type': 'application/json'}

scale = 1 

for j in range(15, 45, 15):
    print("Tasks= ", j)

    for i in range(j):
        response = requests.post(api_endpoint, headers=headers)
        
        response.raise_for_status()
        
        if response.status_code == 200:
            print(f"Request {i+1} successful")
        else:
            print(f"Request {i+1} failed with status code: {response.status_code}")
        
        # exponential distribution
        delay = np.random.exponential(scale)
        time.sleep(delay)

    time.sleep(j*10)
    response = requests.get(url)
    print('------------------------------------------------\n')