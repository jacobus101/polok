# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Colombian localization POS Invoice patch',
    'version': '12.0',
    'author': 'Santiago Lopez',
    'category': 'Point of Sale',
    'depends': [
        'l10n_co_edi_jorels_pos',
    ],
    'summary': 'Patch some functionality from l10n_co_edi_jorels_pos like XMLReceipt document and avoid printing pdf report at POS invoice',
    'data': [
        'views/pos_assets.xml'
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
    'installable': True,
}