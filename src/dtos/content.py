from typing import TypedDict, List


class ContentUpdateDTO(TypedDict, total=False):
    content: str
    images: List[str]


class ContentCreateDTO(TypedDict, total=True):
    page: int
    content: str
    chapter: int
    images: List[str]
