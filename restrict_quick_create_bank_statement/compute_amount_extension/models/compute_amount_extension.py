from odoo import models, api

class AccountInvoice(models.Model):
    _inherit = 'account.invoice' 

    @api.multi
    def call_compute_amount(self):
        for record in self:
            record._compute_amount()
        return True
