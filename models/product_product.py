from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _name = "product.product"
    _description = "Product"
    # _inherit = ["mail.thread", "mail.activity.mixin"]
    # _order = "name, id"

    name = fields.Char(index=True, required=True, translate=True)
    description = fields.Text(translate=True)
    type = fields.Selection(
        selection=[("consu", "Consumable"), ("service", "Service")],
        compute="_compute_type",
        store=True,
        readonly=False,
    )
    quantity = fields.Integer(
        string="Number of price rules",
    )
    product_count = fields.Integer(
        string="# Products",
        compute="_compute_product_count",
        help=_(
            "The number of products under this "
            "category (Does not consider the children categories)"
        ),
    )
    price = fields.Float(
        string="Sales Price",
        default=1.0,
        digits="Product Price",
        help="Price at which the product is sold to customers.",
    )
    volume = fields.Float()
    weight = fields.Float()
    active = fields.Boolean(default=True)
    image_1920 = fields.Image(max_width=1920, max_height=1920)
    image_256 = fields.Image(max_width=256, max_height=256)
    image_128 = fields.Image(max_width=128, max_height=128)
    # company_id = fields.Many2one(comodel_name="res.company", index=1)
    category_id = fields.Many2one(
        comodel_name="product.category",
        required=True,
        help="Select category for the current product",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency", compute="_compute_currency_id"
    )
    attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        relation="product_attribute_value_rel",
        string="Attribute Values",
    )
    # partner_id = self._context.get("partner_id")

    def _compute_product_count(self):
        read_group_res = self.env["product.product"].read_group(
            [("category_id", "child_of", self.ids)],
            ["category_id"],
            ["category_id"],
        )
        group_data = dict(
            (data["category_id"][0], data["category_id_count"])
            for data in read_group_res
        )
        for category in self:
            product_count = 0
            for sub_category_id in category.search(
                [("id", "child_of", category.ids)]
            ).ids:
                product_count += group_data.get(sub_category_id, 0)
            category.product_count = product_count
