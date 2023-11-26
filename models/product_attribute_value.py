from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ProductAttributeValue(models.Model):
    _name = "product.attribute.value"
    _description = "Attribute Value"

    name = fields.Char(string="Value", required=True, translate=True)
    is_used_on_products = fields.Boolean(
        string="Used on Products", compute="_compute_is_used_on_products"
    )
    attribute_id = fields.Many2one(
        comodel_name="product.attribute",
        string="Attribute",
        required=True,
        index=True,
        help=(
            "The attribute cannot be changed once "
            "the value is used on at least one product."
        ),
    )
    product_ids = fields.Many2many(
        comodel_name="product.product",
        relation="product_attribute_value_rel",
        string="Products with this attribute value",
    )

    @api.depends("product_ids")
    def _compute_is_used_on_products(self):
        for attribute_value in self:
            attribute_value.is_used_on_products = bool(
                attribute_value.product_ids
            )

    def write(self, values):
        if "attribute_id" in values:
            for attribute_value in self:
                if (
                    attribute_value.attribute_id.id != values["attribute_id"]
                    and attribute_value.is_used_on_products
                ):
                    raise UserError(
                        _(
                            "You cannot change the attribute "
                            "of the value '%(attribute_name)s' "
                            "because it is used on "
                            "some products: %(product_list)s, ..."
                        )
                        % {
                            "attribute_name": attribute_value.name,
                            "product_list": ", ".join(
                                attribute_value.product_ids.search(
                                    [], limit=10
                                ).mapped("name")
                            ),
                        }
                    )

        res = super().write(values)
        return res

    @api.ondelete(at_uninstall=False)
    def _unlink_except_used_on_product(self):
        for attribute_value in self:
            if attribute_value.is_used_on_products:
                raise UserError(
                    _(
                        "You cannot delete the attribute value "
                        "because it is used on some products"
                    )
                )

    def name_get(self):
        return [
            (value.id, "%s: %s" % (value.attribute_id.name, value.name))
            for value in self
        ]
