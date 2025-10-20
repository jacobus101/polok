# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import AccessError

class AccountMove(models.Model):
    _inherit = "account.move"

    can_user_reset_to_draft = fields.Boolean(
        string="El usuario actual puede restablecer a borrador",
        compute="_compute_can_user_reset_to_draft",
        help="Campo calculado para uso en vista: refleja el permiso del usuario actual.",
    )

    def _compute_can_user_reset_to_draft(self):
        can = self.env.user.can_reset_account_move
        for move in self:
            move.can_user_reset_to_draft = bool(can)

    def button_draft(self):
        """Refuerza la seguridad en backend."""
        if not self.env.user.can_reset_account_move:
            raise AccessError(_("No tiene permiso para restablecer a borrador facturas/asientos."))
        return super().button_draft()
