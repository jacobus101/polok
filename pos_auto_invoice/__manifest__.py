# -*- coding: utf-8 -*-
{
    'name': "POS automatic invoice option",
    'version': '1.0.1',
    'category': 'Point of Sale',
    'author': 'Santiago Lopez',
    'price': '0',
    'sequence': 0,
    'depends': [
        'point_of_sale'
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/parameter_data.xml',
        'template/import_library.xml',
        'views/pos_config.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    "currency": 'USD',
    "external_dependencies": {
        "python": [],
        "bin": []
    },
    'images': ['static/description/icon.png'],
    "license": "OPL-1",
    'installable': True,
    'application': True,
    'post_init_hook': 'auto_action_after_install',
}
