from odoo import models, fields, api

class FormQuickCreateRule(models.Model):
    _name = 'form.quick.create.rule'
    _description = 'Form Quick Create Rules'

    name = fields.Char('Nombre', required=True)
    model_id = fields.Many2one('ir.model', string='Modelo', required=True)
    field_id = fields.Many2one('ir.model.fields', string='Campo', required=True,
        domain="[('model_id', '=', model_id), ('ttype', 'in', ['many2one', 'many2many'])]")
    company_id = fields.Many2one('res.company', string='Compañía',
        default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)
    
    @api.onchange('model_id')
    def _onchange_model_id(self):
        self.field_id = False

    @api.model
    def _disable_quick_create(self):
        """
        Método para deshabilitar la creación rápida en los campos especificados
        """
        rules = self.search([('active', '=', True)])
        for rule in rules:
            if rule.field_id:
                # Modificar el atributo no_create en el campo
                rule.field_id.write({
                    'no_create': True,
                    'no_create_edit': True,
                })
        return True 