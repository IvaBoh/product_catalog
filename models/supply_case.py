from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SupplyCase(models.Model):
    _name = "supply.case"
    _description = "Product supply case"

    supply_date = fields.Date(default=lambda self: fields.Datetime.now())
    supplier_id = fields.Many2one(comodel_name="res.partner")
    item_ids = fields.One2many(
        comodel_name="supply.item",
        inverse_name="case_id",
        string="Products that will be supplied in this case.",
    )

    def name_get(self):
        return [
            (
                record.id,
                "%s: %s" % (record.supplier_id.name, record.supply_date),
            )
            for record in self
        ]
