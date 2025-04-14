from odoo import models, api, fields, _
import logging

_logger = logging.getLogger(__name__)

class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.model
    def check_user_groups(self):
        """Método para verificar los grupos del usuario actual"""
        user = self.env.user
        has_manager_group = user.has_group('account.group_account_manager')
        _logger.info(
            'Usuario %s (ID: %s) verificando permisos - Es manager: %s',
            user.name, user.id, has_manager_group
        )
        
        # Listar todos los grupos del usuario
        groups = user.groups_id
        _logger.info('Grupos del usuario:')
        for group in groups:
            _logger.info('- %s (ID: %s)', group.name, group.id)
            
        return has_manager_group 

class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    check_user_groups = fields.Boolean(
        string='Check User Groups',
        compute='_compute_check_user_groups',
    )

    @api.depends('statement_id')
    def _compute_check_user_groups(self):
        for line in self:
            user = self.env.user
            has_manager_group = user.has_group('account.group_account_manager')
            _logger.info(
                'Usuario %s (ID: %s) verificando permisos - Es manager: %s',
                user.name, user.id, has_manager_group
            )
            
            # Listar todos los grupos del usuario
            groups = user.groups_id
            _logger.info('Grupos del usuario:')
            for group in groups:
                _logger.info('- %s (ID: %s)', group.name, group.id)
                
            line.check_user_groups = has_manager_group 