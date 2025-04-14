from odoo import models, fields, api, _
from odoo.exceptions import AccessError

class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    user_has_accounting_rights = fields.Boolean(
        string='Has Accounting Rights',
        compute='_compute_user_has_accounting_rights',
        store=False,
    )

    @api.depends('user_id')
    def _compute_user_has_accounting_rights(self):
        for record in self:
            record.user_has_accounting_rights = self.env.user.has_group('account.group_account_user')

    @api.model
    def create(self, vals):
        if not self.env.user.has_group('account.group_account_user'):
            if self._context.get('quick_create'):
                raise AccessError(_('No tiene permisos para crear registros rápidos. Por favor, contacte a su administrador.'))
        return super(AccountBankStatement, self).create(vals)

class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    user_has_accounting_rights = fields.Boolean(
        string='Has Accounting Rights',
        compute='_compute_user_has_accounting_rights',
        store=False,
    )

    @api.depends('user_id')
    def _compute_user_has_accounting_rights(self):
        for record in self:
            record.user_has_accounting_rights = self.env.user.has_group('account.group_account_user')

    @api.model
    def create(self, vals):
        if not self.env.user.has_group('account.group_account_user'):
            if self._context.get('quick_create'):
                raise AccessError(_('No tiene permisos para crear líneas rápidas. Por favor, contacte a su administrador.'))
        return super(AccountBankStatementLine, self).create(vals) 