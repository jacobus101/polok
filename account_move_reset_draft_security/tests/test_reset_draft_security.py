# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestResetDraftSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Group = cls.env['res.groups']
        cls.View = cls.env['ir.ui.view']

    def test_group_exists(self):
        group = self.env.ref('account_move_reset_draft_security.group_account_move_reset_to_draft', raise_if_not_found=False)
        self.assertTrue(group, "El grupo de permiso no fue encontrado.")

    def test_view_has_groups_attribute(self):
        # Ensure inherited view exists and contains the groups attribute
        view = self.env.ref('account_move_reset_draft_security.view_move_form_inherit_reset_draft_security', raise_if_not_found=False)
        self.assertTrue(view, "La vista heredada no fue encontrada.")
        arch = view.arch_db or ""
        self.assertIn('account_move_reset_draft_security.group_account_move_reset_to_draft', arch,
                      "La vista no aplica el atributo 'groups' al botón button_draft.")
