from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ProductCategory(models.Model):
    """
    Product category class. Hierarchical class for tree like categories.
    """

    _name = "product.category"
    _description = "Product Category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    name = fields.Char(index=True, required=True)
    complete_name = fields.Char(
        compute="_compute_complete_name",
        recursive=True,
        store=True,
    )
    parent_path = fields.Char(index=True)
    product_count = fields.Integer(
        string="# Products",
        compute="_compute_product_count",
        help="The number of products under this category "
        "(Does not consider the children categories)",
    )
    parent_id = fields.Many2one(
        comodel_name="product.category",
        string="Parent Category",
        index=True,
        ondelete="cascade",
    )
    child_ids = fields.One2many(
        comodel_name="product.category",
        inverse_name="parent_id",
        string="Child Categories",
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        """
        Method that returns complete name for category,
        so name includes ancestor names.
        """
        for category in self:
            if category.parent_id:
                category.complete_name = "%s / %s" % (
                    category.parent_id.complete_name,
                    category.name,
                )
            else:
                category.complete_name = category.name

    def _compute_product_count(self):
        """
        Method that calculate how many products in its category.
        Does not include child categories.
        """
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

    @api.constrains("parent_id")
    def _check_category_recursion(self):
        """
        Method that blocks attempts to create recursive categories.
        """
        if not self._check_recursion():
            raise ValidationError(_("You can't create recursive categories."))

    @api.ondelete(at_uninstall=False)
    def _unlink_disabled_if_product(self):
        """
        Method that disallowed to delete category if category is linked with
        some products
        """
        for category in self:
            if category.product_count > 0:
                raise UserError(
                    _(
                        "You can't delete this category, "
                        "because it contains linked products."
                    )
                )

    @api.model
    def name_create(self, name):
        """
        Special method to set name (not complete name) for the category
        """
        return self.create({"name": name}).name_get()[0]

    def name_get(self):
        """
        Method that returns proper name for attribute value.
        Value without attribute name has no sense.
        """
        if not self.env.context.get("hierarchical_naming", True):
            return [(record.id, record.name) for record in self]
        return super().name_get()
