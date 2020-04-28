# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Website Sale Checkout Extension',
    'summary': 'Extension bringing city dropdown into checkout process',
    'version': '12.0.1.1.0',
    'category': 'Website',
    'author': 'Santiago López',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/website_sale_checkout_city.xml'
    ],
}