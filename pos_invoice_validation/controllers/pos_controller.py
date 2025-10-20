# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import re
import logging

_logger = logging.getLogger(__name__)


class PosInvoiceValidationController(http.Controller):
    """
    Controlador para validación de campos obligatorios para facturación electrónica en el POS
    """

    @http.route('/pos_invoice_validation/get_config', type='json', auth='user', methods=['POST'])
    def get_validation_config(self, pos_config_id=None):
        """
        Endpoint para obtener la configuración de validación del POS
        """
        try:
            if pos_config_id:
                config = request.env['pos.config'].browse(pos_config_id)
            else:
                # Obtener la primera configuración disponible
                config = request.env['pos.config'].search([], limit=1)
            
            if not config.exists():
                # Valores por defecto si no hay configuración
                return {
                    'success': True,
                    'config': {
                        'require_email': True,
                        'require_vat': True,
                        'require_identification_type': True,
                        'require_regime': True,
                        'require_liability': True,
                        'require_municipality': True
                    }
                }
            
            return {
                'success': True,
                'config': {
                    'require_email': config.require_email_for_customers,
                    'require_vat': config.require_vat_for_customers,
                    'require_identification_type': config.require_identification_type_for_customers,
                    'require_regime': config.require_regime_for_customers,
                    'require_liability': config.require_liability_for_customers,
                    'require_municipality': config.require_municipality_for_customers
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': 'Error al obtener configuración',
                'message': str(e)
            }

    @http.route('/pos_invoice_validation/validate_partner', type='json', auth='user', methods=['POST'])
    def validate_partner_fields(self, partner_id, pos_config_id=None):
        """
        Endpoint para validar todos los campos obligatorios de un partner desde el POS
        """
        try:
            partner = request.env['res.partner'].browse(partner_id)
            
            if not partner.exists():
                return {
                    'success': False,
                    'error': 'Cliente no encontrado',
                    'message': 'El cliente seleccionado no existe'
                }
            
            # Obtener configuración de validación
            config_response = self.get_validation_config(pos_config_id)
            if not config_response['success']:
                return config_response
            
            config = config_response['config']
            
            # Validar campos según configuración
            validation_errors = []
            
            if config['require_email']:
                email_validation = self._validate_email(partner.email)
                if not email_validation['valid']:
                    validation_errors.append(email_validation['message'])
            
            if config['require_vat']:
                vat_validation = self._validate_vat(partner.vat)
                if not vat_validation['valid']:
                    validation_errors.append(vat_validation['message'])
            
            if config['require_identification_type']:
                if not partner.l10n_latam_identification_type_id:
                    validation_errors.append('El tipo de identificación es obligatorio para facturación electrónica (DIAN)')
            
            if config['require_regime']:
                if not partner.type_regime_id:
                    validation_errors.append('El régimen fiscal es obligatorio para facturación electrónica (DIAN)')
            
            if config['require_liability']:
                if not partner.type_liability_id:
                    validation_errors.append('La responsabilidad fiscal es obligatoria para facturación electrónica (DIAN)')
            
            if config['require_municipality']:
                if not partner.municipality_id:
                    validation_errors.append('El municipio es obligatorio para facturación electrónica (DIAN)')
            
            if validation_errors:
                return {
                    'success': False,
                    'error': 'Campos obligatorios faltantes',
                    'message': '; '.join(validation_errors),
                    'partner_id': partner.id,
                    'partner_name': partner.name,
                    'can_proceed': False
                }
            
            return {
                'success': True,
                'partner_id': partner.id,
                'partner_name': partner.name,
                'can_proceed': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'message': str(e)
            }

    def _validate_email(self, email):
        """
        Valida el formato del email
        """
        if not email or email.strip() == '':
            return {
                'valid': False,
                'message': 'El correo electrónico es obligatorio para facturación electrónica'
            }
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return {
                'valid': False,
                'message': 'El formato del correo electrónico no es válido. Por favor, ingrese un email válido (ejemplo: usuario@dominio.com)'
            }
        
        return {
            'valid': True,
            'message': 'Email válido'
        }

    def _validate_vat(self, vat):
        """
        Valida el formato del NIT/Documento
        """
        if not vat or vat.strip() == '':
            return {
                'valid': False,
                'message': 'El NIT/Documento de identidad es obligatorio para facturación electrónica (DIAN)'
            }
        
        # Validar formato básico de NIT colombiano (6-15 dígitos)
        vat_clean = re.sub(r'[^0-9]', '', vat)
        if not re.match(r'^[0-9]{6,15}$', vat_clean):
            return {
                'valid': False,
                'message': 'El formato del NIT/Documento no es válido. Debe contener entre 6 y 15 dígitos'
            }
        
        return {
            'valid': True,
            'message': 'NIT/Documento válido'
        }

    @http.route('/pos_invoice_validation/get_partner_data', type='json', auth='public', methods=['POST'])
    def get_partner_data(self):
        """
        Endpoint para obtener los datos completos de un partner por nombre
        """
        # Obtener el parámetro del JSON request
        if hasattr(request, 'jsonrequest') and request.jsonrequest:
            partner_name = request.jsonrequest.get('partner_name')
        else:
            # Fallback para requests normales
            partner_name = request.params.get('partner_name')
        _logger.info("🔍 Recibida petición para obtener datos del partner: %s", partner_name)
        try:
            # Buscar el partner por nombre (sin restricción de empresa)
            partner = request.env['res.partner'].search([
                ('name', 'ilike', partner_name)
            ], limit=1)
            
            _logger.info("🔍 Búsqueda realizada. Partner encontrado: %s", partner.exists())
            
            if not partner.exists():
                _logger.warning("⚠️ No se encontró ningún partner con el nombre '%s'", partner_name)
                return {
                    'success': False,
                    'error': 'Cliente no encontrado',
                    'message': f'No se encontró un cliente con el nombre "{partner_name}"'
                }
            
            _logger.info("✅ Partner encontrado: %s (ID: %s, is_company: %s)", partner.name, partner.id, partner.is_company)
            
            # Obtener datos del partner
            partner_data = {
                'success': True,
                'name': partner.name,
                'email': partner.email or '',
                'vat': partner.vat or '',
                'l10n_latam_identification_type_id': partner.l10n_latam_identification_type_id.id if partner.l10n_latam_identification_type_id else None,
                'type_regime_id': partner.type_regime_id.id if partner.type_regime_id else None,
                'type_liability_id': partner.type_liability_id.id if partner.type_liability_id else None,
                'municipality_id': partner.municipality_id.id if partner.municipality_id else None
            }
            
            _logger.info("📋 Datos del partner: %s", partner_data)
            return partner_data
            
        except Exception as e:
            _logger.error("❌ Error al obtener datos del partner '%s': %s", partner_name, e, exc_info=True)
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'message': str(e)
            }