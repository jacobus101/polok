from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def call_compute_amount(self):
        for record in self:
            record._compute_amount()
        return True
