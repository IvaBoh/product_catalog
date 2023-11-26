from odoo import fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"
    _description = _("Supplier company")

    staff_ids = fields.One2many(
        comodel_name="res.partner", inverse_name="company_id"
    )
