from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SupplyItem(models.Model):
    """
    Class which instance represents supply item entity.
    It is simply describe what products in what quantities should be supplied
    """

    _name = "supply.item"
    _description = _("Supply item is a product presented in some quantity")

    quantity = fields.Integer(default=1)
    product_id = fields.Many2one(comodel_name="product.product", required=True)
    case_id = fields.Many2one(comodel_name="supply.case", string="Supply case")
    active = fields.Boolean(default=True)

    @api.constrains("active")
    def _check_active_and_in_case(self):
        """
        Method that checks if there are supply item connected to some supply
        case. If connected, it blocks supply item archiving
        """
        for item in self:
            if not item.active and item.case_id:
                raise ValidationError(
                    _(
                        "You can't archive the item that "
                        "has been added to supply case."
                    )
                )
