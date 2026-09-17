import json

from pydantic import BaseModel, ConfigDict, Field


class Parser(BaseModel):

    seed: int = Field(default=42, ge=0, le=1000)
    lives: int = Field(default=3, ge=1, le=100000)
    level_max_time: int= Field(default=200, ge=30, le=100000)
    point_per_pacgum: int= Field(default=10, ge=1, le=1000)
    point_per_ghosts: int= Field(default=200, ge=1, le=1000)
    points_per_super_pacgum: int= Field(default=50, ge=0, le=1000)

    model_config = ConfigDict(extra='forbid')

def parse():
    with open("config.json") as f:
        data = json.load(f)
        Parser.model_validate(data)
        print(data)

parse()