from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ProductAttributeValue(models.Model):
    """
    Attribute value class. Attribute could have multiple values.
    Only combination of attribute and its value may have sense.
    """

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
        ondelete="cascade",
    )
    product_ids = fields.Many2many(
        comodel_name="product.product",
        relation="product_attribute_value_rel",
        string="Products with this attribute value",
    )

    @api.depends("product_ids")
    def _compute_is_used_on_products(self):
        """
        Method that sets a bool field on instance if
        some attribute values is used on some products
        """
        for attribute_value in self:
            attribute_value.is_used_on_products = bool(
                attribute_value.product_ids
            )

    def write(self, values):
        """
        Method that blocks attribute value change if it used on some product
        """
        if "attribute_id" in values:
            for attribute_value in self:
                if (
                    attribute_value.attribute_id.id != values["attribute_id"]
                    and attribute_value.is_used_on_products
                ):
                    raise UserError(
                        _(
                            "You can't change the attribute "
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
        """
        Method that blocks attribute value deletion if it used on some product
        """
        for attribute_value in self:
            if attribute_value.is_used_on_products:
                raise UserError(
                    _(
                        "You can't delete the attribute value "
                        "because it is used on some products"
                    )
                )

    def name_get(self):
        """
        Method that returns proper name for attribute value.
        Value without attribute name has no sense.
        """
        return [
            (value.id, "%s: %s" % (value.attribute_id.name, value.name))
            for value in self
        ]
