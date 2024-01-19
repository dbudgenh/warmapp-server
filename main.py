from fastapi import FastAPI, Request
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

@app.get("/items/{item_id}")
async def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}

@app.post("/")
async def read_post(body:dict):
    print(body)
    if 'eventType' in body:
        db.insert(body)
    else:
        print("Else")

    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)          