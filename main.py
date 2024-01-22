from fastapi import FastAPI, Request,HTTPException
from database import MongoDB
import uvicorn

app = FastAPI()
db = MongoDB()

@app.get("/")
async def read_root(req:Request):
    request_args = req.query_params
    if request_args:
        print(request_args)
        return request_args
    else:
        return {"message": "Hello, FastAPI!"}

@app.put("/")
async def read_put():
    print("Put request")

@app.get("/sensorData/{device_id}")
async def get_device(device_id: str):
    result =  db.get_sensor_data_for_device(device_id)
    if not result:
        raise HTTPException(status_code=404,detail="device not found")
    return result

@app.post("/")
async def read_post(body:dict):
    print(body)
    if 'eventType' in body:
        print(body)
        db.insert(body)
    else:
        print("Else")

    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)          