from typing import Union
from pydantic import BaseModel


class Repository(BaseModel):
    name: str


class GitHubEvent(BaseModel):
    id: Union[str, int]
    type: str
    repo: Repository