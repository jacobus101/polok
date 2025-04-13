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

    journal_ids = fields.Many2many(
        'account.journal',
        string='Journals',
        default=lambda self: self._default_journals(),
        required=True,
        readonly=True,
    )
    journal_count = fields.Integer(
        default=lambda self: self._default_journal_count(),
        readonly=True
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        required=True,
        default=lambda self: self._default_journal(),
        domain="[('id', 'in', journal_ids)]",
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
        compute='_compute_currency',
        store=True,
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self._default_company(),
        required=True,
        readonly=True,
    )
    expense_model_id = fields.Many2one(
        'account.reconcile.model',
        string='Expense Type',
        required=True,
        domain="[('journal_id', '=', journal_id)]",
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

    @api.depends('journal_id')
    def _compute_currency(self):
        for record in self:
            if record.journal_id:
                record.currency_id = record.journal_id.currency_id or record.journal_id.company_id.currency_id
            else:
                record.currency_id = record.company_id.currency_id

    @api.onchange('journal_ids')
    def compute_journal_count(self):
        self.journal_count = len(self.journal_ids.ids)

    @api.onchange('journal_id')
    def _onchange_journal(self):
        if self.journal_id:
            return {'domain': {'expense_model_id': [('journal_id', '=', self.journal_id.id)]}}
        return {'domain': {'expense_model_id': []}}

    @api.onchange('expense_model_id')
    def _onchange_expense_model(self):
        if self.expense_model_id:
            self.description = self.expense_model_id.name

    @api.multi
    def _calculate_values_for_statement_line(self, record):
        res = super(CashExpenseWizard, self)._calculate_values_for_statement_line(record)
        res.update({
            'journal_id': self.journal_id.id,
            'partner_id': self.partner_id.id,
            'amount': -abs(self.amount),  # Siempre negativo para pagos
            'date': fields.Date.context_today(self),
            'name': self.description,
            'expense_model_id': self.expense_model_id.id,
        })
        return res 