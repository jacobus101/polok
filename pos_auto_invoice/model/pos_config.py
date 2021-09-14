# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class pos_config(models.Model):
    _inherit = "pos.config"

    pos_auto_invoice = fields.Boolean('POS auto invoice',
                                      help='POS auto to checked to invoice button',
                                      default=1)
