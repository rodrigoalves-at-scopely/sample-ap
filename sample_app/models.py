from dataclasses import dataclass


@dataclass
class Quote:
    id: int
    author: str
    text: str
