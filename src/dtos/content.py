from typing import TypedDict, List


class ContentUpdateDTO(TypedDict, total=False):
    title: str
    content: str
    images: List[str]


class ContentCreateDTO(TypedDict, total=True):
    page: int
    title: str
    content: str
    chapter: int
    images: List[str]
