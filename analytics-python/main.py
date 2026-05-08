
from fastapi import FastAPI
app = FastAPI()

@app.get("/analytics/cpm/{creator_id}")
def get_cpm(creator_id: str):
    return {"creator": creator_id, "cpm": 3.5}
