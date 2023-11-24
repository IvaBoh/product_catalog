from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"
    _description = "Supplier company"

    staff_ids = fields.One2many(
        comodel_name="res.partner", inverse_name="company_id"
    )
