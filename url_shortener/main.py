from fastapi import FastAPI, HTTPException, Request
from url_shortener.routes.shorten import router as ShortenRouter
from url_shortener.routes.redirect import router as RedirectRouter
from mongoengine import connect, disconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from decouple import config
import uvicorn


MONGO_URI = config('MONGO_URI')
app = FastAPI()
templates = Jinja2Templates(directory = "url_shortener/templates")


app.include_router(ShortenRouter, tags = ["Shortify long URL"], prefix = "/api/v1/shortify")
app.include_router(RedirectRouter, tags = ["Redirect to Short URL"])


@app.get("/", response_class = HTMLResponse)
async def index(request : Request):
    return templates.TemplateResponse("index.html", {"request" : request})


@app.on_event("startup")
async def create_db_client():
    try:
        connect(host = MONGO_URI)
    except Exception as e:
        raise HTTPException(status_code= 404, detail = "Database Connection Error!")


@app.on_event("shutdown")
async def shutdown_db_client():
    try:
        disconnect(host = MONGO_URI)
    except Exception as e:
        raise HTTPException(status_code= 404, detail = "Database Connection Error!")
    
    
if __name__ == "__main__":
    uvicorn.run(app, host  = "0.0.0.0", port = 5000)