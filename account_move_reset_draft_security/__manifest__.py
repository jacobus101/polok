# -*- coding: utf-8 -*-
{
    "name": "Account Move Reset to Draft Security",
    "version": "16.0.1.0.0",
    "summary": "Controla el permiso de 'Restablecer a borrador' en facturas mediante una casilla en usuarios.",
    "category": "Accounting/Accounting",
    "author": "Santiago Lopez",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "views/res_users_views.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
    "application": False,
}
