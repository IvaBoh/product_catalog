from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class UpdateProductQtyWizard(models.TransientModel):
    """
    Wizard class that allows to update product quantities.
    It takes info from supply case and update product quantities in simple
    manner.
    """

    _name = "update.product.qty.wizard"
    _description = "Wizard that allows to update product quantities"

    case_id = fields.Many2one(
        comodel_name="supply.case",
        string="Supply case",
        help="Choose supply case to update some product set",
        ondelete="cascade",
    )
    item_ids = fields.Many2many(
        comodel_name="supply.item",
        relation="wizard_supply_item_rel",
        string="Quantities of the these products will be updated",
        compute="_compute_item_ids",
        ondelete="cascade",
    )

    @api.depends("case_id")
    def _compute_item_ids(self):
        """
        This method fill in supply items for wizard model, so they can be
        displayed in two-steps wizard form
        """
        self.ensure_one()
        if self.case_id:
            items = self.env["supply.item"].search(
                [("case_id", "=", self.case_id.id)]
            )
            self.item_ids = [(6, 0, items.ids)]

    @api.constrains("case_id")
    def _check_case_id(self):
        """
        This method ensures that user select some supply case
        """
        self.ensure_one()
        if not self.case_id:
            raise ValidationError(_("Select supply case"))

    def action_open_wizard_part_2(self):
        """
        This action method opens second form of the wizard
        """
        self.ensure_one()
        view_id = self.env.ref(
            "product_catalog.update_product_qty_wizard_view_form_part_two"
        ).id
        return {
            "name": _("Update product quantities"),
            "view_type": "form",
            "view_mode": "tree",
            "views": [(view_id, "form")],
            "res_model": "update.product.qty.wizard",
            "view_id": view_id,
            "type": "ir.actions.act_window",
            "res_id": self.id,
            "target": "new",
        }

    def update_product_qty(self):
        """
        This action button method from the second wizard form updates the
        products base on the supply case info and its supply items
        """
        self.ensure_one()
        supply_items = self.env["supply.item"].browse(self.item_ids.ids)
        for supply_item in supply_items:
            product = supply_item.product_id
            quantity_to_add = supply_item.quantity

            new_quantity = product.quantity + quantity_to_add
            product.write({"quantity": new_quantity})

        message = (
            f"Product quantities updated for "
            f"the case: '{self.case_id.name_get()[0][1]}'."
        )
        if self.case_id:
            self.case_id.write({"active": False})

        notification = {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Product update info"),
                "message": message,
                "type": "success",
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
        return notification
