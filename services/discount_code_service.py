from data import discount_code_db
from models.campaign import Campaign
from models.coupon import Coupon


class DiscountCodeService:
    def __init__(self):
        self.DB = discount_code_db.DiscountCodeDB()

    def get_coupon(self, for_customer, coupon_id):
        coupon = self.DB.coupons.get(coupon_id)
        if coupon and coupon.customer_id == for_customer:
            return coupon

    def get_campaign_coupons(self, for_brand, campaign_id):
        campaign = self.DB.campaigns.get(campaign_id)
        if campaign and campaign.brand_id == for_brand:
            coupons = []
            for id, coupon in self.DB.coupons.items():
                if coupon.campaign_id == campaign_id:
                    coupons.append(coupon)
            return coupons

    def acquire_coupon(self, for_customer, from_brand):
        campaign_id = None
        for id, campaign in self.DB.campaigns.items():
            if campaign.brand_id == from_brand:
                campaign_id = id
                break

        if campaign_id:
            for id, coupon in self.DB.coupons.items():
                if coupon.campaign_id == campaign_id and not coupon.customer_id:
                    coupon.customer_id = for_customer
                    return coupon

    def create_campaign(self, for_brand, coupon_ct, percentage_discount):
        campaign = Campaign(for_brand)
        self.DB.campaigns[campaign.id] = campaign

        for x in range(coupon_ct):
            coupon = Coupon(campaign.id, percentage_discount)
            self.DB.coupons[coupon.id] = coupon

        return campaign
