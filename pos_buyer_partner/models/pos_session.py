from odoo import models, _

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _orders_missing_buyer(self):
        return self.order_ids.filtered(
            lambda o: not o.buyer_partner_id and o.state not in ('cancel')
        )

    def _popup(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Pedidos sin Comprador'),
            'res_model': 'pos.session.buyer.check.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_session_id': self.id,
                'default_missing_order_count': len(self._orders_missing_buyer()),
            }
        }

    def action_pos_session_close(self):
        self.ensure_one()
        if self._orders_missing_buyer() and not self.env.context.get('ignore_missing_buyer'):
            return self._popup()
        return super(PosSession, self).action_pos_session_close()

    def action_pos_session_validate(self):
        self.ensure_one()
        if self._orders_missing_buyer() and not self.env.context.get('ignore_missing_buyer'):
            return self._popup()
        return super(PosSession, self).action_pos_session_validate()
