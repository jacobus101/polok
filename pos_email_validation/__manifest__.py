{
    'name': 'POS Email Validation',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Validate email format in POS client form',
    'description': """
        This module adds email format validation to the Point of Sale client form.
    """,
    'author': 'Santiago López',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_email_validation_templates.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_email_validation/static/src/js/pos_email_validation.js',
        ],
    },
    'installable': True,
    'application': False,
}
