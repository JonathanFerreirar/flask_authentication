from typing import TypedDict, Optional


class ChapterUpdateDTO(TypedDict, total=False):
    title: Optional[str]
    chapter_number: int


class ChapterCreateDTO(TypedDict, total=True):
    title: str
    etech: int
    chapter_number: int
