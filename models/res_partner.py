from odoo import fields, models


class ResPartner(models.Model):
    """
    Inherited model huge res_partner model
    Don't need any additional functionality
    """

    _inherit = "res.partner"
    _description = "Product supplier"

    is_supplier = fields.Boolean(default=True)
    company_id = fields.Many2one(comodel_name="res.company")
