odoo.define('pos_default_partner_avoid_edit.disable_edit_button', function(require) {
    'use strict';

    var screens = require('point_of_sale.screens');

    screens.ClientListScreenWidget.include({
        display_client_details: function(visibility, partner, clickpos) {
            this._super(visibility, partner, clickpos);
            var editButton = this.$('.edit-buttons');
            var defaultPartnerId = this.pos.config.default_partner_id;

            if (partner && partner.id === defaultPartnerId) {
                editButton.hide();
            } else {
                editButton.show();
            }
        },
    });
});
