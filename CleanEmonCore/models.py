"""Essential models definition for CleanEmon"""
import dataclasses
import json
from dataclasses import dataclass
from dataclasses import asdict
from typing import List
import orjson

@dataclass
class EnergyData:
    date: str = ""
    energy_data: List[dict] = dataclasses.field(default_factory=list)

    def as_json(self, *, string):
        as_dict = asdict(self)

        if string:
            return orjson.dumps(as_dict)
        else:
            return as_dict
