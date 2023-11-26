from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Product supplier"

    is_supplier = fields.Boolean(default=True)
    company_id = fields.Many2one(comodel_name="res.company")
