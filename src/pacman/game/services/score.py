from pydantic import BaseModel, TypeAdapter


class ScoreEntry(BaseModel):
    """Represent one persisted leaderboard entry."""

    pseudo: str
    score: int


user_list_adapter = TypeAdapter(list[ScoreEntry])
