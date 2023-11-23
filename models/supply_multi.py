from odoo import fields, models, api


class SupplyMulti(models.Model):
    _name = "supply.multi"
    _description = "Product supply case"

    supplier_id = fields.Many2one(comodel_name="res.partner")
    product_id = fields.Many2one(comodel_name="product.product")
    supply_date = fields.Date()
    quantity = fields.Integer()
