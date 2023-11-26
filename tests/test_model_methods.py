from odoo.tests import tagged
from odoo.exceptions import AccessError, UserError, ValidationError

from .common import TestCommon


@tagged("post_install", "-at_install", "catalog")
class TestModelMethods(TestCommon):
    def test_product_attribute(self):
        # test unlink() if attribute is linked to some product
        with self.assertRaises(UserError):
            self.attribute_material.unlink()

        test_attribute = self.env["product.attribute"].create(
            {
                "name": "Density",
            }
        )
        self.assertTrue(
            test_attribute.unlink(),
            msg="User can delete attribute that doesn't linked to any product.",
        )

    def test_product_attribute_value(self):
        # test unlink() if attribute value is linked to some attribute
        with self.assertRaises(UserError):
            self.attribute_value_material_gold.unlink()

        test_attribute_value = self.attribute_value_weight_30 = self.env[
            "product.attribute.value"
        ].create({"name": "60", "attribute_id": self.attribute_weight.id})

        self.assertTrue(
            test_attribute_value.unlink(),
            msg="User can delete attribute that doesn't linked to any product.",
        )

    def test_product_category(self):
        # test unlink() if category has some linked product(s)
        with self.assertRaises(UserError):
            self.category_spoon.unlink()

        test_category = (
            self.env["product.category"]
            .with_user(self.catalog_user)
            .create({"name": "Test Category"})
        )

        self.assertTrue(test_category.unlink())

        # check category recursion ban
        with self.assertRaises(UserError):
            self.category_spoon.update(
                {"child_ids": [(4, self.category_spoon.id, 0)]}
            )

    def test_product_product(self):
        # check product quantity for the service product and consumable product

        # default product has type 'consu'
        self.assertTrue(self.product_gold_spoon.type == "consu")

        # check quantity for the consumable product
        self.product_gold_spoon._check_quantity()

        # check quantity for the service type
        # qty > 1
        with self.assertRaises(ValidationError):
            product_service_1 = self.env["product.product"].create(
                {
                    "name": "Some service",
                    "type": "service",
                    "quantity": 2,
                    "category_id": self.category_spoon.id,
                }
            )
            product_service_1._check_quantity()
        # qty == 1
        product_service_2 = self.env["product.product"].create(
            {
                "name": "Some service",
                "type": "service",
                "quantity": 1,
                "category_id": self.category_spoon.id,
            }
        )
        product_service_2._check_quantity()

    def test_supply_case(self):
        # check if case contains supply items (1 or more)
        self.supply_case._check_item_quantity()

        # check if case doesn't contain more than 50 items
        items_51 = [
            self.env["supply.item"].create(
                {"product_id": self.product_gold_spoon.id, "quantity": 2}
            )
            for i in range(1, 52)
        ]
        with self.assertRaises(ValidationError):
            self.supply_case.write(
                {
                    "supplier_id": self.supplier_demo.id,
                    "supply_date": "2024-12-12",
                    "item_ids": [
                        (
                            6,
                            0,
                            [new_item.id for new_item in items_51],
                        )
                    ],
                }
            )

        # check case date is today of future
        with self.assertRaises(ValidationError):
            self.env["supply.case"].create(
                {
                    "supplier_id": self.supplier_demo.id,
                    "supply_date": "2022-12-12",
                    "item_ids": [
                        (
                            6,
                            0,
                            [
                                self.supply_item.id,
                            ],
                        )
                    ],
                }
            )
        test_supply_case = self.env["supply.case"].create(
            {
                "supplier_id": self.supplier_demo.id,
                "supply_date": "2100-12-12",
                "item_ids": [
                    (
                        6,
                        0,
                        [
                            self.supply_item.id,
                        ],
                    )
                ],
            }
        )
        test_supply_case._check_case_date()

    def test_supply_item(self):
        """
        Check that supply item that have been already added to supply case
        can't be archived
        """
        self.assertTrue(self.supply_item.active)

        with self.assertRaises(ValidationError):
            self.supply_item.active = False

        # check supply item with no supply case could be archived
        test_supply_item = self.env["supply.item"].create(
            {
                "product_id": self.product_gold_spoon.id,
                "quantity": 10,
            }
        )
        test_supply_item.active = False
        test_supply_item._check_active_and_in_case()
