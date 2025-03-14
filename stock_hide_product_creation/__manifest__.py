{
    'name': 'Hide Product Creation in Order Forms',
    'version': '16.0.1.0.0',
    'category': 'Sales/Purchase/Inventory',
    'summary': 'Disables quick creation, creation, and editing of products in stock picking, purchase order, and sales order forms.',
    'description': """
This module disables the ability to quickly create, create, or edit products from the following forms:
- Stock Picking: Hides these actions in the move lines.
- Purchase Order: Removes the create and edit options in order lines.
- Sales Order: Prevents both template and variant creation or editing actions in order lines.
By enforcing these restrictions, users are limited to selecting only existing products.
""",
    'author': 'Santiago Lopez',
    'license': 'AGPL-3',
    'depends': ['stock', 'purchase', 'sale_management'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
}
