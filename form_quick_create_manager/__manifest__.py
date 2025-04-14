{
    'name': 'Form Quick Create Manager',
    'version': '12.0.1.0.0',
    'category': 'Tools',
    'summary': 'Manage quick create permissions in forms',
    'author': 'Polok',
    'website': 'https://www.polok.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale',
        'stock',
    ],
    'data': [
        'security/form_quick_create_security.xml',
        'security/ir.model.access.csv',
        'views/form_quick_create_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
} 