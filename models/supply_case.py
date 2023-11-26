from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SupplyCase(models.Model):
    _name = "supply.case"
    _description = "Product supply case"

    supply_date = fields.Date(default=lambda self: fields.Date.today())
    supplier_id = fields.Many2one(
        comodel_name="res.partner",
        required=True,
        domain="[('is_company', '=', True)]",
    )
    item_ids = fields.One2many(
        comodel_name="supply.item",
        inverse_name="case_id",
        string="Products that will be supplied in this case.",
    )
    active = fields.Boolean(default=True)

    @api.constrains("supply_date")
    def _check_case_date(self):
        for case in self:
            if not case.supply_date >= fields.Date.today():
                raise ValidationError(
                    _("Supply can be only today or in future.")
                )

    @api.constrains("item_ids")
    def _check_item_quantity(self):
        for record in self:
            if len(record.item_ids) >= 50:
                raise ValidationError(
                    _(
                        "One supply case can't contain "
                        "more than 50 supply items."
                    )
                )
            if len(record.item_ids) == 0:
                raise ValidationError(
                    _("Supply case has to contain supplied items.")
                )

    def name_get(self):
        return [
            (
                record.id,
                "%s: %s" % (record.supplier_id.name, record.supply_date),
            )
            for record in self
        ]
