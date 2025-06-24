{
    "name": "Colombia VAT Auto & Validation",
    "version": "12.0.1.0.0",
    "category": "Localization",
    "author": "Santiago López",
    "license": "AGPL-3",
    "summary": "Generación y validación automática del VAT en Colombia",
    "depends": [
        "base",
        "base_vat",
        "account",
        "l10n_co_edi_jorels",
        "point_of_sale"
    ],
    "data": [
        "views/res_partner_views.xml",
        "views/pos_assets.xml"
    ],
    'qweb': [
        'static/src/xml/pos_partner_fields.xml',
        'static/src/xml/pos_hide_vat.xml'
    ],
    "installable": True,
    "application": False
}
