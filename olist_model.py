from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base
Base = declarative_base()

class ProductCategory(Base):
    __tablename__ = "product_category_name_translation"
    product_category_name=Column(String, primary_key=True, index=True)
    product_category_name_english=Column(String)
    product_category_name_french=Column(String)

    def __str__(self):
        return f"ProductCategory[{self.product_category_name}]"

    def to_json(self):
        return {'product_category_name': self.product_category_name,
                'product_category_name_english': self.product_category_name_english,
                'product_category_name_french': self.product_category_name_french,
                }

    # setter sur champ product_category_name_french
    def set_FR(self, x):
        self.product_category_name_french = x

    # getter champ product_category_name_french
    def get_FR(self):
        return self.product_category_name_french

    def is_filled(self):
        return self.product_category_name_english!='' and self.product_category_name_french!='' and self.product_category_name_french is not None and self.product_category_name_english is not None
