{
    'name': 'Restrict Quick Create in Bank Statements',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Restricts quick create functionality in bank statements for users without accounting permissions',
    'author': 'Polok',
    'website': 'https://www.polok.com',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [
        'views/account_bank_statement_views.xml',
        'security/bank_statement_security.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
} 