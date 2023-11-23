from odoo import fields, models


class ProductAttribute(models.Model):
    _name = "product.attribute"
    _description = "Product Attribute"

    name = fields.Char(string="Attribute", required=True, translate=True)
    value_ids = fields.One2many(
        comodel_name="product.attribute.value",
        inverse_name="attribute_id",
        string="Values",
        copy=True,
    )
