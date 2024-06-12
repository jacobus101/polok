odoo.define('pos_default_partner_avoid_edit.disable_edit_button', function(require) {
    'use strict';

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');

    models.load_fields('res.partner', ['is_default']);

    screens.ClientListScreenWidget.include({
        display_client_details: function(visibility, partner, clickpos) {
            this._super(visibility, partner, clickpos);
            var editButton = this.$('.edit-buttons');

            if (partner.is_default) {
                editButton.hide();
            } else {
                editButton.show();
            }
        },
    });
});
