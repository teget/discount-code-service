from models.base import Base


class Brand(Base):
    def __init__(self, name):
        super().__init__()
        self.name = name
