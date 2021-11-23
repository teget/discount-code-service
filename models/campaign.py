from models.base import Base


class Campaign(Base):
    def __init__(self, brand_id):
        super().__init__()
        self.brand_id = brand_id
