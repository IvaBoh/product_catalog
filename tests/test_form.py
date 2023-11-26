from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import Form

from .common import TestCommon


@tagged("post_install", "-at_install", "catalog")
class TestForm(TestCommon):
    def test_product_quantity_based_on_type(self):
        # check product of service type is single
        product_service_2 = self.env["product.product"].create(
            {
                "name": "Some service",
                "type": "service",
                "quantity": 1,
                "category_id": self.category_spoon.id,
            }
        )
        product_form = Form(product_service_2)
        self.assertEqual(product_form.quantity, 1)

        # change quantity in form
        product_form.quantity = 10
        # check if _onchange_type change quantity back
        product_form.type = "consu"
        product_form.type = "service"
        self.assertEqual(product_form.quantity, 1)
