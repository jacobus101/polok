from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CashExpenseWizard(models.TransientModel):
    _name = 'cash.expense.wizard'
    _inherit = 'cash.box.out'
    _description = 'Cash Expense Wizard'

    def _default_value(self, default_function):
        active_model = self.env.context.get('active_model', False)
        if active_model:
            active_ids = self.env.context.get('active_ids', False)
            return default_function(active_model, active_ids)
        return None

    def _default_company(self):
        return self._default_value(self.default_company)

    def _default_currency(self):
        return self._default_value(self.default_currency)

    def _default_journals(self):
        return self._default_value(self.default_journals)

    def _default_journal(self):
        journals = self._default_journals()
        if journals and len(journals.ids) > 0:
            return self.env['account.journal'].browse(journals.ids[0]).ensure_one()

    def _default_journal_count(self):
        return len(self._default_journals().ids)

    statement_id = fields.Many2one(
        'account.bank.statement',
        string='Statement',
        required=True,
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        required=True,
        default=lambda self: self._default_journal(),
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
        default=lambda self: self._default_currency(),
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self._default_company(),
        required=True,
        readonly=True,
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

    def default_company(self, active_model, active_ids):
        return self.env[active_model].browse(active_ids)[0].company_id

    def default_currency(self, active_model, active_ids):
        return self.default_company(active_model, active_ids).currency_id

    def default_journals(self, active_model, active_ids):
        return self.env[active_model].browse(active_ids)[0].journal_id

    @api.onchange('expense_type')
    def _onchange_expense_type(self):
        domain = [('user_type_id.type', '=', 'expense')]
        if self.expense_type == 'purchase':
            domain = [('user_type_id.type', '=', 'payable')]
        return {'domain': {'expense_account_id': domain}}

    @api.multi
    def _calculate_values_for_statement_line(self, record):
        res = super(CashExpenseWizard, self)._calculate_values_for_statement_line(record)
        res.update({
            'statement_id': self.statement_id.id,
            'journal_id': self.journal_id.id,
            'partner_id': self.partner_id.id,
            'amount': -abs(self.amount),  # Siempre negativo para pagos
            'date': fields.Date.context_today(self),
            'name': self.description,
            'account_id': self.expense_account_id.id,
        })
        return res

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