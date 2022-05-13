"""Essential models definition for CleanEmon"""

import json
from dataclasses import dataclass
from dataclasses import asdict
from typing import List


@dataclass
class EnergyData:
    date: str
    energy_data: List[dict]

    def as_json(self):
        return json.dumps(asdict(self))
