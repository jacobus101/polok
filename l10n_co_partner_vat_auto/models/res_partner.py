# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

class ResPartner(models.Model):
    _inherit = 'res.partner'

    check_digit = fields.Char(
        string='Dígito de Verificación test', size=1,
        help='Solo aplica para NIT con validación')

    identification_document = fields.Char(
        string='Número de documento',
        help='Número base del documento de identificación')
    
    document_type_code = fields.Char(
        string="Document Type Code",
        related='type_document_identification_id.code',
        store=False,
        readonly=True
    )

    @api.onchange('country_id', 'identification_document', 'check_digit', 'type_document_identification_id')
    def _onchange_generate_vat(self):
        _logger = logging.getLogger(__name__)
        if self.country_id and self.identification_document:
            country_code = self.country_id.code
            if not country_code:
                raise ValidationError(_('El país seleccionado no tiene código ISO.'))

            doc_type = self.document_type_code
            vat_number = self.vat

            if doc_type and doc_type == '31':
                if self.check_digit:
                    self.vat = country_code + self.identification_document + self.check_digit
                else:
                    self.vat = country_code + self.identification_document
            elif doc_type and doc_type == '43':
                self.check_digit = False
                self.vat = 'CO' + self.identification_document
            else:
                self.check_digit = False
                self.vat = country_code + self.identification_document
        elif not self.identification_document and self.vat:
            self.vat = False

    def check_vat_co(self, vat):
        vat = vat.replace('-', '').replace('.', '')
        if len(vat) < 4:
            return False
        try:
            int(vat)
        except ValueError:
            return False
        if vat.startswith('44444') and 4001 <= int(vat[5:]) <= 9000:
            return True
        prime = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
        suma = sum(int(vat[i]) * prime[len(vat) - 2 - i] for i in range(len(vat) - 1))
        expected_dv = 11 - (suma % 11) if suma % 11 > 1 else suma % 11
        return str(expected_dv) == vat[-1]
