from typing import TypedDict, List, Optional


class EtechUpdateDTO(TypedDict, total=False):
    title: Optional[str]
    image: Optional[str]
    price: Optional[float]
    language: Optional[str]
    description: Optional[str]
    topics: Optional[List[str]]
    is_published: Optional[float]


class EtechCreateDTO(TypedDict, total=True):
    user: int
    title: str
    image: str
    price: float
    language: str
    topics: List[str]
    description: str
