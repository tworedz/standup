from datetime import date
from datetime import datetime
from datetime import time
from typing import List
from typing import Optional

from pydantic import BaseModel


class FilmSettingSchema(BaseModel):
    telegram_channel_id: int
    film_id: Optional[int]
    cron: str
    timeout: int


class FilmSettingUpdateOrCreateSchema(BaseModel):
    film_id: Optional[int]
    cron: str = "*/5 * * * *"
    timeout: int = 30


class BookSchema(BaseModel):
    movie_id: int
    c_id: int
    discount_2: Optional[float]
    rec_date: Optional[datetime]
    discount_1: Optional[float]
    is_disabled: bool
    price: Optional[float]
    cinema: str
    disable_sales: bool
    hall: str
    time: str
    date: str
    disable_reservation: bool
    cinema_id: int
    hall_id: int
    id: int

    def __str__(self):
        return f"{self.cinema} ({self.hall}) - {self.date} в {self.time}"


class BookResponse(BaseModel):
    list: List[BookSchema]
    result: Optional[int]


class FilmSchema(BaseModel):
    name: str
    voteCount: Optional[int]


class Cinema(BaseModel):
    dates: List[str] = []
    cinema: str
