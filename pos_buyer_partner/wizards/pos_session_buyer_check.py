from odoo import models, fields

class PosSessionBuyerCheckWizard(models.TransientModel):
    _name = 'pos.session.buyer.check.wizard'
    _description = 'Aviso pedidos sin comprador'

    session_id = fields.Many2one('pos.session', required=True, readonly=True)
    missing_order_count = fields.Integer(readonly=True)

    def action_close_anyway(self):
        return self.session_id.with_context(ignore_missing_buyer=True).action_pos_session_close()
