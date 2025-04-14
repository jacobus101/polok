from odoo import models, fields, api, _
from odoo.exceptions import AccessError

class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.model
    def create(self, vals):
        if not self.env.user.has_group('account.group_account_user'):
            if self._context.get('quick_create'):
                raise AccessError(_('No tiene permisos para crear registros rápidos. Por favor, contacte a su administrador.'))
        return super(AccountBankStatement, self).create(vals)

class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    @api.model
    def create(self, vals):
        if not self.env.user.has_group('account.group_account_user'):
            if self._context.get('quick_create'):
                raise AccessError(_('No tiene permisos para crear líneas rápidas. Por favor, contacte a su administrador.'))
        return super(AccountBankStatementLine, self).create(vals) 