{
    'name': 'Account Cash Expense',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Create cash payments for direct expenses',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_cash_invoice',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/cash_expense_wizard_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
} 