from analyse import analyse
from flask import jsonify
import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse
app = FastAPI()

@app.post("/analyse")
async def index(input):
    return analyse(input)
@app.get("/")
async def read_index():
    return FileResponse('index.html')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4030)