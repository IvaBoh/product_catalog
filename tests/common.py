from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):
    def setUp(self):
        super(TestCommon, self).setUp()

        self.product_catalog_group_user = self.env.ref(
            "product_catalog.product_catalog_group_user"
        )
        self.product_catalog_group_admin = self.env.ref(
            "product_catalog.product_catalog_group_admin"
        )
        self.catalog_user = self.env["res.users"].create(
            {
                "name": "Catalog User",
                "login": "catalog_user",
                "groups_id": [
                    (4, self.product_catalog_group_user.id),
                ],
            }
        )
        self.catalog_admin = self.env["res.users"].create(
            {
                "name": "Catalog Admin",
                "login": "catalog_admin",
                "groups_id": [
                    (4, self.product_catalog_group_admin.id),
                ],
            }
        )
        self.supplier_demo = self.env["res.partner"].create(
            {"name": "Demo Supplier"}
        )
        self.company_demo = self.env["res.company"].create(
            {"name": "Demo Company"}
        )
        self.attribute_material = self.env["product.attribute"].create(
            {
                "name": "Material",
            }
        )
        self.attribute_weight = self.env["product.attribute"].create(
            {
                "name": "Weight",
            }
        )
        self.attribute_value_material_gold = self.env[
            "product.attribute.value"
        ].create({"name": "Gold", "attribute_id": self.attribute_material.id})
        self.attribute_value_weight_30 = self.env[
            "product.attribute.value"
        ].create({"name": "30", "attribute_id": self.attribute_weight.id})
        self.category_spoon = self.env["product.category"].create(
            {
                "name": "Spoons",
            }
        )
        self.product_gold_spoon = self.env["product.product"].create(
            {
                "name": "Teaspoon",
                "description": "Spoon for tea cups",
                "quantity": 10,
                "price": 6000,
                "category_id": self.category_spoon.id,
                "attribute_value_ids": [
                    (
                        6,
                        0,
                        [
                            self.attribute_value_material_gold.id,
                            self.attribute_value_weight_30.id,
                        ],
                    )
                ],
            }
        )
        self.supply_item = self.env["supply.item"].create(
            {
                "product_id": self.product_gold_spoon.id,
                "quantity": 10,
            }
        )
        self.supply_case = self.env["supply.case"].create(
            {
                "supplier_id": self.supplier_demo.id,
                "supply_date": "2023-12-12",
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
