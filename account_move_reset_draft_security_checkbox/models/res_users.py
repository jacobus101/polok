# -*- coding: utf-8 -*-
from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    can_reset_account_move = fields.Boolean(
        string="Puede restablecer facturas a borrador",
        help="Si está activo, este usuario puede ejecutar la acción 'Restablecer a borrador' en facturas/asientos.",
        default=False,
    )
