# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    require_email_for_customers = fields.Boolean(
        string='Requerir Email para Clientes',
        default=True,
        help='Si está activado, se requerirá email para todos los clientes del POS'
    )
    
    require_vat_for_customers = fields.Boolean(
        string='Requerir NIT/Documento para Clientes',
        default=True,
        help='Si está activado, se requerirá NIT/Documento para todos los clientes del POS'
    )
    
    require_identification_type_for_customers = fields.Boolean(
        string='Requerir Tipo de Identificación para Clientes',
        default=True,
        help='Si está activado, se requerirá tipo de identificación para todos los clientes del POS'
    )
    
    require_regime_for_customers = fields.Boolean(
        string='Requerir Régimen Fiscal para Clientes',
        default=True,
        help='Si está activado, se requerirá régimen fiscal para todos los clientes del POS'
    )
    
    require_liability_for_customers = fields.Boolean(
        string='Requerir Responsabilidad Fiscal para Clientes',
        default=True,
        help='Si está activado, se requerirá responsabilidad fiscal para todos los clientes del POS'
    )
    
    require_municipality_for_customers = fields.Boolean(
        string='Requerir Municipio para Clientes',
        default=True,
        help='Si está activado, se requerirá municipio para todos los clientes del POS'
    )
    
    @api.model
    def get_validation_config(self):
        """Obtener configuración de validación para el POS"""
        config = self.env['pos.config'].browse(self.env.context.get('pos_config_id', False))
        if not config:
            # Si no hay configuración específica, usar valores por defecto
            return {
                'require_email': True,
                'require_vat': True,
                'require_identification_type': True,
                'require_regime': True,
                'require_liability': True,
                'require_municipality': True
            }
        
        return {
            'require_email': config.require_email_for_customers,
            'require_vat': config.require_vat_for_customers,
            'require_identification_type': config.require_identification_type_for_customers,
            'require_regime': config.require_regime_for_customers,
            'require_liability': config.require_liability_for_customers,
            'require_municipality': config.require_municipality_for_customers
        }

