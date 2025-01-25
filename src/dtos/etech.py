from typing import TypedDict, List, Optional


class EtechUpdateDTO(TypedDict, total=False):
    title: Optional[str]
    image: Optional[str]
    price: Optional[float]
    topics: Optional[List[str]]
    description: Optional[str]


class EtechCreateDTO(TypedDict, total=True):
    user: int
    title: str
    image: str
    price: float
    topics: List[str]
    description: str
