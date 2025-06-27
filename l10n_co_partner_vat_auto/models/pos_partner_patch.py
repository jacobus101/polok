# -*- coding: utf-8 -*-
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class ResPartnerPosPatch(models.Model):
    _inherit = 'res.partner'

    @staticmethod
    def _co_compute_vat(vals):
        if not isinstance(vals, dict):
            return vals
        if vals.get('vat'):
            return vals
        doc = vals.get('identification_document')
        if not doc:
            return vals
        code = vals.get('l10n_co_document_type')
        if code == 'rut' and vals.get('check_digit'):
            vals['vat'] = 'CO%s%s' % (doc, vals['check_digit'])
        else:
            vals['vat'] = 'CO%s' % doc
        return vals

    def _normalize(self, data):
        if not data:
            return []
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
        return []

    @api.model
    def create_from_ui(self, partners):
        for p in self._normalize(partners):
            self._co_compute_vat(p)
        return super(ResPartnerPosPatch, self.with_context(from_pos=True).sudo()).create_from_ui(partners)

    @api.model
    def write_from_ui(self, partners):
        for p in self._normalize(partners):
            self._co_compute_vat(p)
        return super(ResPartnerPosPatch, self.with_context(from_pos=True).sudo()).write_from_ui(partners)

    @api.multi
    def write(self, vals):
        if self.env.context.get('from_pos'):
            return super(ResPartnerPosPatch, self.sudo()).write(vals)
        return super(ResPartnerPosPatch, self).write(vals)
