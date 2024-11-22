from fastapi import FastAPI
import dht
import uvicorn
from models.comera_control import Relay
import relay as relay


app = FastAPI()

@app.get('/')
def root():
    return {'message': 'hello form raspberry pi'}

@app.get('/sensors/temp')
def get_dht():
   temp, humidity = dht.read_dht22()
   return {'Temperature': temp, 'Humidity': humidity}

@app.post('/sensors/relay')
def control_camera(model: Relay):
    result =  relay.control_camera(model.camera_id, model.action)
    return {"action": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
