from pydantic import BaseModel, TypeAdapter


class ScoreEntry(BaseModel):
    pseudo: str
    score: int


user_list_adapter = TypeAdapter(list[ScoreEntry])
