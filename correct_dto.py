# dto написанное не chatGpt
from datetime import datetime
from typing import List

from pydantic import BaseModel
from pydantic.v1 import Field


class SimpleLocation(BaseModel):
    city: str = Field(..., enum=["MOSCOW", "SPB", "NULL"])
    name: str
    address: str
    """city: str = Field(..., enum=["MOSCOW", "SPB", "NULL"]) Эта строка объявляет атрибут (поле) city типа str.
    city: str: Указывает, что атрибут city будет строкой.
    = Field(..., enum=["MOSCOW", "SPB", "NULL"]): Это используется для более тонкой настройки поля.
    ...: Это эллипсис (Ellipsis), означающий, что поле city является обязательным (не может быть None).
    enum=["MOSCOW", "SPB", "NULL"]: Определяет допустимые значения для поля city. При попытке присвоить значение, отличное от 
    “MOSCOW”, “SPB” или “NULL”, pydantic выдаст ошибку валидации."""


class SimpleEventDto(BaseModel):
    name: str
    description: str
    location: SimpleLocation
    id: str
    type: Field(..., enum=["EVENT", "REPEAT", "PLACE"])
    times: List[datetime]
    """times: List[datetime]: Эта часть объявляет атрибут с именем times. Он имеет тип List[datetime], 
    что означает, что это список (List) объектов типа datetime (объекты даты и времени из модуля datetime).
    = Field(..., alias="times"): Это вызов функции Field из pydantic. 
    Эта функция используется для добавления метаданных к атрибуту модели.
    ...: Это эллипсис (...), который в данном контексте означает “использовать значения по умолчанию”.
     То есть, он не задает явно значение по умолчанию для атрибута times, оставляя его необязательным.
    alias="times": Это ключевое слово alias, которое указывает, что имя атрибута в исходных данных 
    (например, в JSON-ответе от API) может отличаться от имени атрибута в модели Pydantic. 
    В данном случае, alias="times" говорит, что если в JSON будет поле с именем “times”,
     Pydantic должен использовать это поле для заполнения атрибута times модели."""
    allImages: List[List[bytes]] = Field(default_factory=list, alias="allImages") # Requires additional handling
    mainImage: List[bytes] = Field(default_factory=list, alias="mainImage") # Requires additional handling
    price: str # или price: Optional[str] если поле price необязательное
    tags: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)
    priceType: str = Field(..., enum=["PRICELESS", "TICKET", "HOUR", "AVERAGE_BILL"])
    shortDescription: str # или price: Optional[str] если поле price необязательное
