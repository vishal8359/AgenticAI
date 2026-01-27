from fastapi import FastAPI
import uvicorn
import random
import time

app = FastAPI(title="Temperature Simulator")

@app.get('/temperature')
def get_temp():
    # step 1 : Simulate sensor display
    time.sleep(2)

    # step 2 : Generate random temperature
    temp = round(random.uniform(20.0, 35.0), 2)
    return {"temperature : ": temp}