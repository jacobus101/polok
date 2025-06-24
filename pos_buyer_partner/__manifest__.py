{
    "name": "POS Buyer Partner",
    "summary": "Sets buyer_partner_id only when customer differs from default POS partner (depends on pos_default_partner).",
    "version": "12.0.5.0.0",
    "author": "ChatGPT",
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
        "pos_default_partner"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/pos_order_views.xml",
        "views/pos_session_wizard.xml"
    ],
    "installable": True,
    "application": False
}
