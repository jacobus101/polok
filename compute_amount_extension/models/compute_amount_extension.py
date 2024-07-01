from odoo import models, api

class YourModel(models.Model):
    _inherit = 'AccountInvoice' 

    @api.multi
    def call_compute_amount(self):
        for record in self:
            record._compute_amount()
