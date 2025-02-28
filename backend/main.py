from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI News API is running!"}