from fastapi import APIRouter, HTTPException
from url_shortener.schemas import UrlSchema 
from url_shortener.models import Url
import os
import shortuuid 
from decouple import config

router = APIRouter()

@router.post('/', response_model = dict) 
async def test(url : UrlSchema):
    url = dict(url)
    
    shortCode = shortuuid.ShortUUID().random(length = 7)
    if (url["customCode"]): shortCode = url["customCode"]

    # short URL by joining host to shortCode
    shortUrl = os.path.join(config("HOST"), shortCode)

    # database already uses that shortCode
    urlExists = Url.objects(shortCode = shortCode)
    if urlExists: raise HTTPException(status_code = 400, detail = "Short code is invalid, It has been used.")

    try:
        url = Url( longUrl = url["longUrl"], shortCode = shortCode, shortUrl = shortUrl )
        url.save()

        return {
            "message" : "Successfully shortened URL.",
            "shortUrl" : shortUrl,
            "longUrl" : url["longUrl"]
        }
        
    except Exception as e: raise HTTPException(status_code = 500, detail = "Unknown Error")
