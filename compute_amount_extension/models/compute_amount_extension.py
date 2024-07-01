from odoo import models, api

class YourModel(models.Model):
    _inherit = 'account._compute_amount' 

    @api.multi
    def call_compute_amount(self):
        for record in self:
            record._compute_amount()
