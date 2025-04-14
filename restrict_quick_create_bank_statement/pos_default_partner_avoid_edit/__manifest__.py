# __manifest__.py
{
    'name': 'POS Default Partner Avoid Edit',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Disable edit button when default partner is selected in POS',
    'description': """
        This module disables the edit button in the POS interface when the default partner is selected.
    """,
    'author': 'Santiago López',
    'depends': ['point_of_sale', 'pos_default_partner'],
    'data': [
        'views/pos_assets.xml',
    ],
    'qweb': [
        'static/src/xml/pos_default_partner_avoid_edit.xml',
    ],
    'installable': True,
    'application': False,
}
