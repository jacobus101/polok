from odoo import models, fields, api
from odoo.exceptions import UserError

class PosOrder(models.Model):
    _inherit = 'pos.order'

    buyer_partner_id = fields.Many2one('res.partner', string='Buyer')

    @api.model
    def _order_fields(self, ui_order):
        """Set buyer_partner_id only when the customer selected by the cashier
        is different from the default POS customer defined by pos_default_partner.
        """
        vals = super(PosOrder, self)._order_fields(ui_order)

        partner_id = ui_order.get('partner_id')
        session = self.env['pos.session'].browse(ui_order.get('pos_session_id'))
        default_partner = session.config_id.default_partner_id

        if partner_id and default_partner and partner_id != default_partner.id:
            vals['buyer_partner_id'] = partner_id
        else:
            # Make it explicit for clarity
            vals['buyer_partner_id'] = False
        return vals

    def write(self, vals):
        if 'buyer_partner_id' in vals:
            for order in self:
                if order.state == 'done' and not self.env.user._is_superuser():
                    raise UserError('No puedes modificar el comprador en una orden cerrada.')
        return super(PosOrder, self).write(vals)
