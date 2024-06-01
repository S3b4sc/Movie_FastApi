from pydantic import BaseModel, Field
from typing import Optional


#Movie model ---------------------------------

class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field( min_length=5 , max_length=15)
    overview:str = Field( min_length=15 , max_length=50 )
    year:int =  Field( le=2022 )
    rating:float = Field(ge=1, le=10.0)
    category:str = Field(min_length=5 , max_length=15)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
               {
                'id': 1,
                'title' : 'Crepusculo',
                'overview' : 'The twilight is almost better than sunday',
                'year' : '2022',
                'rating' : 9.5,
                'category' : 'Phantasy'
            }
            ]
        }
    }
