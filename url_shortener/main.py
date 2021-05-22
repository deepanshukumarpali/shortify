from fastapi import FastAPI, HTTPException, Request, Form
from url_shortener.routes.shorten import router as ShortenRouter, shortme
from url_shortener.routes.redirect import router as RedirectRouter
from mongoengine import connect, disconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from decouple import config
import uvicorn


MONGO_URI = config('MONGO_URI')
app = FastAPI()

templates = Jinja2Templates(directory = "url_shortener/templates")
app.mount("/static", StaticFiles(directory="url_shortener/static"), name="static")


app.include_router(ShortenRouter, tags = ["Shortify long URL"], prefix = "/api/v1/shortify")
app.include_router(RedirectRouter, tags = ["Redirect to Short URL"])


@app.get("/", response_class = HTMLResponse)
async def index(request : Request):
    return templates.TemplateResponse("index.html", {"request" : request,})


@app.post("/", response_class = HTMLResponse)
async def shortMe(request: Request, longUrl: str = Form(...), customCode: str = Form(...)):
    
    try:
        response = shortme({
            'longUrl' : longUrl,
            'customCode' : customCode
        })
    except HTTPException as e:
        response = {
            'longUrl' : longUrl,
            'customCode' : customCode,
            'shortUrl' : e.detail
        }
    finally:
        return templates.TemplateResponse("index.html", {
            "request" : request,
            "longUrl" : longUrl,
            "customCode" : customCode,
            "shortUrl" : response['shortUrl']
        })


@app.on_event("startup")
async def create_db_client():
    try:
        connect(host = MONGO_URI)
    except Exception as e:
        raise HTTPException(status_code= 404, detail = "Database Connection Error!")


@app.on_event("shutdown")
async def shutdown_db_client(): 
    pass
    
    
if __name__ == "__main__":
    uvicorn.run(app, host  = "0.0.0.0", port = 5000)
    # uvicorn url_shortener.main:app --reload