# -*- coding: utf-8 -*-
{
    "name": "POS: Ocultar botón de facturar en órdenes POS",
    "summary": "Oculta el botón 'Invoice' en pos.order; visible solo para equipo administrativo.",
    "version": "16.0.1.0.0",
    "author": "Santiago Lopez",
    "license": "LGPL-3",
    "category": "Point of Sale",
    "depends": ["point_of_sale"],
    "data": [
        "security/pos_hide_invoice_button_groups.xml",
        "views/pos_order_form.xml",
    ],
    "application": False,
    "installable": True,
    "description": """
Este módulo nació porque los vendedores, al necesitar imprimir una copia de la factura,
ingresaban primero por la Orden POS. Si la factura aún no estaba generada, sin querer
la creaban presionando el botón 'Invoice' (acción action_pos_order_invoice) desde la
interfaz de la orden POS. Para evitar errores operativos y duplicidades, este módulo
oculta dicha acción en la interfaz gráfica para todos los usuarios, dejándola visible
únicamente al equipo administrativo con permisos técnicos.
""",
}
