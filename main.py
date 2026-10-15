from fastapi import FastAPI


app = FastAPI(title="Smart Support API")


@app.get("/")
def home():
    return {"message": "Smart Support API çalışıyor."}
