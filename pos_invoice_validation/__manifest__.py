# -*- coding: utf-8 -*-
{
    'name': 'POS Invoice Validation',
    'version': '16.0.1.0.0',
    'summary': 'Bloquea la validación del pedido en el POS si el cliente no tiene VAT/NIT.',
    'category': 'Point of Sale',
    'author': 'Santiago + ChatGPT',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [
        'models/res_partner.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_invoice_validation/static/src/js/vat_blocker.js',
            'pos_invoice_validation/static/src/js/partner_validation.js',
        ],
    },
    'installable': True,
}
