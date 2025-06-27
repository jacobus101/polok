# models/pos_partner_patch.py
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class ResPartnerPosPatch(models.Model):
    _inherit = 'res.partner'

    @staticmethod
    def _co_compute_vat(vals):
        """Añade VAT en vals si falta."""
        if not isinstance(vals, dict):
            return vals                # defensivo: ignorar valores atípicos
        if vals.get('vat'):
            return vals                # ya está
        doc = vals.get('identification_document')
        _logger.info("Valor de doc: %s", doc)
        if not doc:
            return vals
        code = vals.get('l10n_co_document_type')
        _logger.info("Valor de code: %s", code)
        if code == 'rut' and vals.get('check_digit'):
            vals['vat'] = 'CO%s%s' % (doc, vals['check_digit'])
        else:
            vals['vat'] = 'CO%s' % doc
        return vals

    # helpers para normalizar el argumento -------------------------------
    def _normalize(self, data):
        """Siempre devuelve una lista de dicts."""
        if not data:
            return []
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
        # Caso extremo: string u otro tipo
        return []

    @api.model
    def create_from_ui(self, partners):
        for p in self._normalize(partners):
            self._co_compute_vat(p)
        return super().create_from_ui(partners)

    @api.model
    def write_from_ui(self, partners):
        for p in self._normalize(partners):
            self._co_compute_vat(p)
        return super().write_from_ui(partners)
