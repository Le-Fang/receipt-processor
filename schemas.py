from marshmallow import Schema, fields
from marshmallow.validate import Regexp

class ItemSchema(Schema):
    shortDescription = fields.String(required=True, validate=Regexp(r"^[\w\s\-]+$"))
    price = fields.String(required=True, validate=Regexp(r"^\d+\.\d{2}$"))

class ReceiptSchema(Schema):
    retailer = fields.String(required=True, validate=Regexp(r"^[\w\s\-&]+$"))
    purchaseDate = fields.Date(required=True)
    purchaseTime = fields.String(required=True, validate=Regexp(r"^\d{2}:\d{2}$"))
    items = fields.List(fields.Nested(ItemSchema), required=True, validate=lambda x: len(x) > 0)
    total = fields.String(required=True, validate=Regexp(r"^\d+\.\d{2}$"))