from odoo import fields, models, _


class SupplyItem(models.Model):
    _name = "supply.item"
    _description = _("Supply item is a product presented in some quantity")

    quantity = fields.Integer(default=1)
    product_id = fields.Many2one(comodel_name="product.product", required=True)
    case_id = fields.Many2one(comodel_name="supply.case", string="Supply case")
