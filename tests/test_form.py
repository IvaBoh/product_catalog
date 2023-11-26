from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import Form

from common import TestCommon


@tagged("post_install", "-at_install", "catalog")
class TestForm(TestCommon):
    def test_book_taken_date(self):
        book_form = Form(self.book_demo)

        book_form.reader_id = self.library_user.partner_id
        self.assertEqual(book_form.taken_date, fields.Date.today())

        book_form.reader_id = self.library_user.partner_id
        self.assertEqual(book_form.taken_date, fields.Date.today())

    def test_book_default_get(self):
        book_form = Form(self.book_demo)

        # check default type
        self.assertEqual(book_form.type, "book")

        # check type change
        self.book_demo.write({"type": "brochure"})
        book_form = Form(self.book_demo)
        self.assertEqual(book_form.type, "brochure")
