# -*- coding: utf-8 -*-
{
    "name": "Account Move Reset to Draft Security (User Checkbox)",
    "version": "16.0.1.0.0",
    "summary": "Controla 'Restablecer a borrador' con una casilla en Usuarios, más bloqueo en backend.",
    "category": "Accounting/Accounting",
    "author": "Santiago Lopez",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "views/res_users_views.xml",
        "views/account_move_views.xml",
        "security/ir.model.access.csv"
    ],
    "installable": True,
    "application": False
}
