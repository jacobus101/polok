from odoo import api, fields, models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    expense_model_id = fields.Many2one(
        'account.reconcile.model',
        string='Expense Model',
        readonly=True,
    )

    @api.multi
    def fast_counterpart_creation(self):
        for st_line in self:
            if not st_line.expense_model_id:
                return super(AccountBankStatementLine, st_line).fast_counterpart_creation()
            
            model = st_line.expense_model_id
            vals = {
                'name': st_line.name,
                'debit': st_line.amount < 0 and -st_line.amount or 0.0,
                'credit': st_line.amount > 0 and st_line.amount or 0.0,
                'account_id': model.account_id.id,
                'partner_id': st_line.partner_id.id,
            }
            st_line.process_reconciliation(new_aml_dicts=[vals]) 