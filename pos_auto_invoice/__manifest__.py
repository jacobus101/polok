# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Autoselect POS Invoice',
    'version': '12.0',
    'author': 'OCA',
    'category': 'Point of Sale',
    'depends': [
        'l10n_co_edi_jorels_pos',
    ],
    'summary': 'Autoselect invoice options at POS orders',
    'data': [
        'views/pos_assets.xml',
        'views/pos_config_view.xml',
    ],
    'installable': True,
}
