{
    'name': 'Ocultar creación/edición rápida de productos en Stock Picking',
    'version': '16.0.1.0.0',
    'category': 'Stock',
    'summary': 'Oculta la creación rápida y la opción de crear/editar productos en los formularios de stock.picking',
    'author': 'Santiago Lopez',
    'license': 'AGPL-3',
    'depends': ['stock', 'purchase', 'sale_management'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
}
