# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.exceptions import AccessError

class AccountMove(models.Model):
    _inherit = "account.move"

    def button_draft(self):
        """Bloquea el reset a borrador si el usuario no tiene el grupo permitido."""
        if not self.env.user.has_group("account_move_reset_draft_security.group_account_move_reset_to_draft"):
            raise AccessError(_("No tiene permiso para restablecer a borrador facturas/asientos."))
        return super().button_draft()
