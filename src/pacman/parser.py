import json
import re

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
        raw_data = f.read()
        first_clean = re.sub(r'//.*', '', raw_data)
        second_clean = re.sub(r'#.*', '', first_clean)

    cleaned_data = json.loads(second_clean)
    data = Parser.model_validate(cleaned_data)
    return data
    # to handle later the try except properly in main with pydantic error and file not found error