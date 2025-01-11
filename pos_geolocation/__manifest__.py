{
    'name': 'POS Geolocation',
    'version': '1.0',
    'summary': 'Adds geolocation functionality to the POS',
    'description': """
        This module adds geolocation tracking to Point of Sale orders.
    """,
    'author': 'Santiago López',
    'website': 'https://polok.co',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_order_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_geolocation/static/src/js/pos_geolocation.js',
            'pos_geolocation/static/src/js/pos_geolocation_button.js',
            'pos_geolocation/static/src/xml/pos_geolocation_button.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
