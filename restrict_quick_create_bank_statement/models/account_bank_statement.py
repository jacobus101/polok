from odoo import models, api, _
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