from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Status": "Alive", "Message": "If you see this, Vercel is working!"}

@app.get("/ping")
def ping():
    return "pong"
