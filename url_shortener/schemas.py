from typing import Optional
from pydantic import BaseModel, constr

class UrlSchema(BaseModel):
    longUrl : str 
    customCode : Optional[constr(max_length = 20)] = None
