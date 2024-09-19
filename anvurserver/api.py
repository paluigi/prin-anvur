import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()


@app.get("/v1/anvur/")
def journals() -> dict[str, str]:
    with open("db.json", "r") as file:
        data = json.load(file)
    json_compatible_item_data = jsonable_encoder(data)
    return JSONResponse(content=json_compatible_item_data)
