from odoo import fields, models, api


class SupplyItem(models.Model):
    _name = "supply.item"
    _description = "Supply item is a product presented in some quantity"

    quantity = fields.Integer(default=1)
    product_id = fields.Many2one(comodel_name="product.product", required=True)
    case_id = fields.Many2one(comodel_name="supply.case", string="Supply case")
