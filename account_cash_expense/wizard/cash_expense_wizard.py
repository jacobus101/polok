from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CashExpenseWizard(models.TransientModel):
    _name = 'cash.expense.wizard'
    _description = 'Cash Expense Wizard'

    statement_id = fields.Many2one(
        'account.bank.statement',
        string='Statement',
        required=True,
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        required=True,
        domain=[('type', 'in', ['purchase', 'general'])],
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
    )
    amount = fields.Monetary(
        string='Amount',
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    expense_type = fields.Selection([
        ('purchase', 'Purchase'),
        ('expense', 'Expense'),
    ], string='Type', required=True, default='expense')
    expense_account_id = fields.Many2one(
        'account.account',
        string='Expense Account',
        required=True,
        domain=[('user_type_id.type', 'in', ['payable', 'expense'])],
    )
    description = fields.Char(
        string='Description',
        required=True,
    )

    @api.onchange('expense_type')
    def _onchange_expense_type(self):
        domain = [('user_type_id.type', '=', 'expense')]
        if self.expense_type == 'purchase':
            domain = [('user_type_id.type', '=', 'payable')]
        return {'domain': {'expense_account_id': domain}}

    def create_statement_line(self):
        self.ensure_one()
        vals = {
            'statement_id': self.statement_id.id,
            'journal_id': self.journal_id.id,
            'partner_id': self.partner_id.id,
            'amount': -abs(self.amount),  # Siempre negativo para pagos
            'date': fields.Date.context_today(self),
            'name': self.description,
            'account_id': self.expense_account_id.id,
        }
        self.env['account.bank.statement.line'].create(vals)
        return {'type': 'ir.actions.act_window_close'} 