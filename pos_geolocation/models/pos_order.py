from odoo import models, fields

class PosOrder(models.Model):
    _inherit = 'pos.order'

    latitude = fields.Float(string="Latitude", help="Geolocation Latitude")
    longitude = fields.Float(string="Longitude", help="Geolocation Longitude")
