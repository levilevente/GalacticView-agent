from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """
    A simple root endpoint.
    """
    return {"Hello": "World"}