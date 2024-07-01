from odoo import models, api

class YourModel(models.Model):
    _inherit = 'account'  # Reemplaza 'your.model' con el nombre del modelo existente

    @api.multi
    def call_compute_amount(self):
        for record in self:
            record._compute_amount()
