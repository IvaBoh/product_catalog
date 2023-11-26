from odoo.tests import tagged
from odoo.exceptions import AccessError

from .common import TestCommon


@tagged("post_install", "-at_install", "catalog")
class TestAccessRights(TestCommon):
    def test_product_catalog_user_access_rights(self):
        with self.assertRaises(
            AccessError,
            msg="Catalog user can read only the categories"
            " created by him due to rule 'product_catalog_rule_user'",
        ):
            self.category_spoon.with_user(self.catalog_user).read()

        # user can create categories
        test_category = (
            self.env["product.category"]
            .with_user(self.catalog_user)
            .create({"name": "Test Category"})
        )

        # user can't change his own or other users created categories
        with self.assertRaises(
            AccessError, msg="Catalog user can't edit any category"
        ):
            self.category_spoon.with_user(self.catalog_user).write(
                {"name": "New Category Name"}
            )
            test_category.with_user(self.catalog_user).write(
                {"name": "New Category Name"}
            )

        # user can delete hiw own categories
        test_category.with_user(self.catalog_user).unlink()

        # user can't delete other user categories
        with self.assertRaises(
            AccessError,
            msg="Catalog user can't delete other user categories "
            "due to rule 'product_catalog_rule_user'",
        ):
            self.category_spoon.with_user(self.catalog_user).unlink()

    def test_product_catalog_admin_access_rights(self):
        # admin can create
        admin_category = (
            self.env["product.category"]
            .with_user(self.catalog_admin)
            .create({"name": "Admin Created Category"})
        )

        # admin can read everything in product.catalog model
        test_category = (
            self.env["product.category"]
            .with_user(self.catalog_user)
            .create({"name": "User Created Category"})
        )
        test_category.with_user(self.catalog_admin).read()
        self.category_spoon.with_user(self.catalog_admin).read()

        # admin can update everything
        self.category_spoon.with_user(self.catalog_admin).write(
            {"name": "New Category Name"}
        )
        test_category.with_user(self.catalog_admin).write(
            {"name": "New Category Name"}
        )

        # admin can delete his and others categories
        # if category has no products
        test_category.with_user(self.catalog_admin).unlink()
        admin_category.with_user(self.catalog_admin).unlink()
