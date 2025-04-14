from odoo import models, fields, api, _

class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    def action_create_cash_expense(self):
        self.ensure_one()
        action = {
            'name': _('Create Cash Expense'),
            'type': 'ir.actions.act_window',
            'res_model': 'cash.expense.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_statement_id': self.id,
            }
        }
        return action 