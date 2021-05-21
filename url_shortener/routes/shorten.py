from fastapi import APIRouter, HTTPException
from url_shortener.schemas import UrlSchema
from url_shortener.models import Url
import os
import shortuuid 
from decouple import config

router = APIRouter()

@router.post('/', response_model = dict) 
async def shorten_url(url : UrlSchema):
    url = dict(url)
    shortme(url)
    
def shortme(url):
    shortCode = url["customCode"]
    urlExists = Url.objects(shortCode = shortCode)

    while(urlExists):
        shortCode = shortuuid.ShortUUID().random(length = 7)
        urlExists = Url.objects(shortCode = shortCode)
    
    shortUrl = os.path.join(config("HOST"), shortCode)
    
    try:
        url = Url( longUrl = url["longUrl"], shortCode = shortCode, shortUrl = shortUrl )
        url.save()
        return {
            "message" : "Successfully shortened URL.",
            "shortUrl" : shortUrl,
            "longUrl" : url["longUrl"]
        }
    
    except Exception: 
        
        raise HTTPException(status_code = 500, detail = "Unknown Error")
