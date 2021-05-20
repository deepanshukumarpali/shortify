from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.responses import RedirectResponse
from url_shortener.models import Url
from decouple import config

router = APIRouter()

@router.get("/{short_code}")
async def redirect_url(short_code : str):
    url = Url.objects( shortCode = short_code)
    
    # database does not uses that shortCode
    if not url: raise HTTPException(status_code= 404, detail = "URL not found !")

    url = url[0].to_mongo().to_dict()
    return  RedirectResponse(url = url["longUrl"])
    
