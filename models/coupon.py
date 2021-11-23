import uuid

from models.base import Base


class Coupon(Base):
    def __init__(self, campaign_id, percent_discount):
        super().__init__()
        self.code = str(uuid.uuid4())
        self.campaign_id = campaign_id
        self.percent_discount = percent_discount
        self.customer_id = None
