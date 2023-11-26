from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ProductAttribute(models.Model):
    _name = "product.attribute"
    _description = "Product Attribute"

    name = fields.Char(string="Attribute", required=True, translate=True)
    value_ids = fields.One2many(
        comodel_name="product.attribute.value",
        inverse_name="attribute_id",
        string="Values",
        copy=True,
    )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_used_on_product(self):
        for attribute in self:
            used_attr = attribute.value_ids
            if used_attr:
                raise UserError(
                    _(
                        "You can't delete the attribute "
                        "because it is used on some products"
                    )
                )
