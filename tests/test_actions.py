from odoo.tests import tagged
from odoo.exceptions import AccessError, UserError

from .common import TestCommon


@tagged("post_install", "-at_install", "catalog")
class TestAccessRights(TestCommon):
    def test_action_take_in(self):
        self.book_demo.write({"reader_id": self.library_user.partner_id.id})

        # A library user can't return a book himself
        with self.assertRaises(UserError):
            self.book_demo.with_user(self.library_user).action_take_in()

        # A library admin can return a book
        self.book_demo.with_user(self.library_admin).action_take_in()
        self.assertFalse(self.book_demo.reader_id)

    def test_action_scrap_book(self):
        self.book_demo.with_user(self.library_admin).action_scrap_book()

        self.assertFalse(
            self.book_demo.active,
            "Library admin can archive a book.",
        )

        # library_book_rule_user <field name="perm_write" eval="True"/>
        # eval=True to not rise the error

        # self.book_demo_2 = (
        #     self.env["library.book"]
        #     .with_user(self.library_admin)
        #     .create({"name": "Demo Book 2", "user_id": self.library_admin.id})
        # )
        #
        # with self.assertRaises(AccessError):
        #     self.book_demo_2.with_user(self.library_user).action_scrap_book()
        #
        # self.assertTrue(
        #     self.book_demo_2.active,
        #     "Library user can't archive a book.",
        # )
