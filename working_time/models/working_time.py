# Copyright (C) 2016 Roberto Barreiro (<roberto@disgal.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class res_partner_working_time(models.Model):
    _name = "res.partner.working.time"
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', ondelete='cascade', select=True, domain=['|',('is_company','=',True),('parent_id','=',False)]),
        'days': fields.char('Days'),
        'morning': fields.char('Morning'),
        'afternoon': fields.char('Afternoon'),
    }

class res_company(models.Model):
    _inherit = "res.company"
    _columns = {
        'schedule': fields.one2many('res.partner.working.time', 'partner_id', 'Working Time'),
    }

class res_partner(models.Model):
    _inherit = "res.partner"
    _columns = {
        'schedule': fields.one2many('res.partner.working.time', 'partner_id', 'Working Time'),
    }
