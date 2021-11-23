import json
import uuid


class Base:
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
