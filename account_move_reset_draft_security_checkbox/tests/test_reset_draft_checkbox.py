# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestResetDraftCheckbox(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User = cls.env['res.users']
        cls.View = cls.env['ir.ui.view']

    def test_user_field_exists(self):
        self.assertIn('can_reset_account_move', self.User._fields)

    def test_move_compute_flag_exists(self):
        self.assertIn('can_user_reset_to_draft', self.env['account.move']._fields)

    def test_view_inherited(self):
        view = self.env.ref('account_move_reset_draft_security_checkbox.view_move_form_inherit_reset_draft_security', raise_if_not_found=False)
        self.assertTrue(view, "La vista heredada de account.move no fue encontrada.")
