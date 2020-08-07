# Copyright (C) 2016 Roberto Barreiro (<roberto@disgal.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Working Time',
    'version': '12.0.0.1',
    'category': 'Website',
    'sequence': 10,
    'summary': 'Show your working time on contact form. It also manages partners working time',
    'description': """
    Manage working time of your partners.
    Show your own working time on website contact form.
    """,
    'author': 'Roberto Barreiro',
    'website': 'https://bitbucket.org/disgalmilladoiro/',
    'depends': ['website_crm',],
    'data': ['views/working_time_form.xml',
             'views/working_time.xml',],
    'installable': True,
    'auto_install': False,
    'application': False,
}
