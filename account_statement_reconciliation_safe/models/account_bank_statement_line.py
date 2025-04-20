from odoo import models, _
from odoo.exceptions import UserError

class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    def process_reconciliation(self, counterpart_aml_dicts=None, payment_aml_rec=None, new_aml_dicts=None):
        """ Versión ajustada: ignora líneas ya conciliadas en lugar de lanzar error. """
        counterpart_aml_dicts = counterpart_aml_dicts or []
        payment_aml_rec = payment_aml_rec or self.env['account.move.line']
        new_aml_dicts = new_aml_dicts or []

        # Filtrar líneas ya conciliadas
        original_len = len(counterpart_aml_dicts)
        counterpart_aml_dicts = [
            d for d in counterpart_aml_dicts
            if not d.get('move_line', self.env['account.move.line']).reconciled
        ]

        if original_len != len(counterpart_aml_dicts):
            reconciled_skipped = original_len - len(counterpart_aml_dicts)
            _logger = self.env['ir.logging']
            _logger.info(f"[ReconciliationSafe] {reconciled_skipped} líneas ya estaban conciliadas y fueron ignoradas.")

        # Si no hay nada para conciliar, no hacemos nada
        if not counterpart_aml_dicts and not new_aml_dicts and not payment_aml_rec:
            return self.env['account.move']  # No hay nada por hacer

        # Llamar a la implementación original (padre)
        return super(AccountBankStatementLine, self).process_reconciliation(
            counterpart_aml_dicts=counterpart_aml_dicts,
            payment_aml_rec=payment_aml_rec,
            new_aml_dicts=new_aml_dicts,
        )
