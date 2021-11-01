# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PosConfig(models.Model):
    _inherit = 'pos.config'

    auto_invoice = fields.Boolean("Auto Invoice", config_parameter='pos_auto_invoice.auto_invoice')
    invoice_type_setting = fields.Selection([
        ('pos_invoice', 'POS invoice'),
        ('electronic_invoice', 'Electronic Invoice')
        ])

    @api.onchange('auto_invoice')
    def _onchange_auto_invoice(self):
        if not self.auto_invoice:
            self.invoice_type_setting = False
        if self.auto_invoice and not self.invoice_type_setting:
            self.invoice_type_setting = 'pos_invoice'
