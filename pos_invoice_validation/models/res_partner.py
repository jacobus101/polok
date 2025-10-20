from odoo import models, fields, api
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _validate_email_format(self, email):
        """Valida el formato del email"""
        if not email or email.strip() == '':
            return False
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return bool(re.match(email_regex, email.strip()))

    @api.model
    def create(self, vals):
        """Bloquea la creación si faltan datos obligatorios"""
        # Validar email si se proporciona
        if vals.get('email') and not self._validate_email_format(vals.get('email')):
            raise models.ValidationError(
                "El formato del correo electrónico no es válido. "
                "Use el formato: ejemplo@dominio.com"
            )
        
        return super().create(vals)

    def write(self, vals):
        """Bloquea la actualización si faltan datos obligatorios"""
        # Validar email si se proporciona
        if vals.get('email') and not self._validate_email_format(vals.get('email')):
            raise models.ValidationError(
                "El formato del correo electrónico no es válido. "
                "Use el formato: ejemplo@dominio.com"
            )
        
        return super().write(vals)
