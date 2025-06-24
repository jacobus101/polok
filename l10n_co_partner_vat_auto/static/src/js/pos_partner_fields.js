odoo.define('l10n_co_partner_vat_auto.pos_partner_fields', function (require) {
    'use strict';

    const models = require('point_of_sale.models');
    const fieldNames = [
        'identification_document',
        'check_digit',
    ];

    // Agregar los campos personalizados al modelo partner
    models.load_fields('res.partner', fieldNames);
}); 