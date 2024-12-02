import json

import requests
from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Optional
from datetime import datetime

# Этот файл как пример - не используется в боте

class SimpleLocation(BaseModel):
    city: str = Field(..., enum=["MOSCOW", "SPB", "NULL"])
    name: str
    address: str


class SimpleEventDto(BaseModel):
    name: str
    description: str
    location: SimpleLocation
    id: str
    type: str = Field(..., enum=["EVENT", "REPEAT", "PLACE"])
    times: List[datetime] = Field(..., alias="times") #alias for correct parsing from API
    allImages: List[List[bytes]] = Field(default_factory=list, alias="allImages") # Requires additional handling
    mainImage: List[bytes] = Field(default_factory=list, alias="mainImage") # Requires additional handling
    price: Optional[str]
    tags: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)
    priceType: str = Field(..., enum=["PRICELESS", "TICKET", "HOUR", "AVERAGE_BILL"])
    shortDescription: Optional[str]

    @validator("times", pre=True)
    def parse_times(cls, value):
        return [datetime.fromisoformat(item) for item in value] if isinstance(value, list) else []


class AfishaParserAPI:
    BASE_URL = "https://AfishaParser"

    def __init__(self):
        pass

    def get_events_for_day(self, unix_time_date: int, page_number: int, page_size: int) -> List[SimpleEventDto]:
      """Получает события за день."""
      params = {
          "unix_time_date": unix_time_date,
          "page_number": page_number,
          "page_size": page_size,
      }
      url = f"{self.BASE_URL}/tg/bot/api/events/day"
      return self._make_request(url, params, SimpleEventDto)


    def get_events_for_week(self, unix_time_monday: int, page_number: int, page_size: int) -> List[SimpleEventDto]:
      """Получает события за неделю."""
      params = {
          "unix_time_monday": unix_time_monday,
          "page_number": page_number,
          "page_size": page_size,
      }
      url = f"{self.BASE_URL}/tg/bot/api/events/week"
      return self._make_request(url, params, SimpleEventDto)

    def _make_request(self, url: str, params: dict, model: BaseModel) -> List[BaseModel]:
        """Вспомогательная функция для выполнения запроса и обработки ответа."""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Проверка кода ответа (200 OK)
            data = response.json()
            # Обработка allImages и mainImage  (НЕОБХОДИМА ДОПОЛНИТЕЛЬНАЯ ЛОГИКА)

            if isinstance(data, list):
                return [model.model_validate(item) for item in data]  #валидация каждой записи
            else:
                return [model.model_validate(data)] #валидация единственной записи
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка HTTP запроса: {e}") from e
        except json.JSONDecodeError as e:
            raise Exception(f"Ошибка разбора JSON: {e}") from e
        except ValidationError as e:
            raise Exception(f"Ошибка валидации данных: {e}") from e


# Пример использования:
api = AfishaParserAPI()

try:
    events = api.get_events_for_day(unix_time_date=1678886400, page_number=1, page_size=10)
    for event in events:
        print(event)
except Exception as e:
    print(f"Ошибка: {e}")