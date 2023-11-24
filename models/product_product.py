from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _name = "product.product"
    _description = "Product"
    # _inherit = ["mail.thread", "mail.activity.mixin"]
    # _order = "name, id"

    name = fields.Char(index=True, required=True, translate=True)
    description = fields.Text(translate=True)
    type = fields.Selection(
        selection=[("consu", "Consumable"), ("service", "Service")],
        string="Product Type",
        default="consu",
        required=True,
        help="Consumable products have to be stored somewhere.",
    )
    quantity = fields.Integer(required=True, default=1)
    price = fields.Float(
        string="Sales Price",
        default=1.0,
        digits=(10, 2),
        help="Price at which the product is sold to customers.",
    )
    active = fields.Boolean(default=True)
    image_1920 = fields.Image(max_width=500, max_height=500)
    image_256 = fields.Image(max_width=256, max_height=256)
    category_id = fields.Many2one(
        comodel_name="product.category",
        required=True,
        help="Select category for the current product",
    )
    attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        relation="product_attribute_value_rel",
        string="Product attributes",
    )

    @api.constrains("quantity", "type")
    def _check_quantity(self):
        for record in self:
            if record.type == "service" and record.quantity > 1:
                raise ValidationError(
                    _(
                        "Only products with type 'Consumable' "
                        "could have quantity more than 1."
                    )
                )
