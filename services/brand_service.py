from data import brand_db


class BrandService:
    def __init__(self):
        self.DB = brand_db.BrandDB()

    def get_brand_by_id(self, brand_id):
        return self.DB.brands.get(brand_id)