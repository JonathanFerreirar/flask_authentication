from typing import TypedDict


class CommentDTO(TypedDict, total=True):
    user: int
    etech: int
    comment: str
