odoo.define('pos_email_validation', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');

    function validateEmail(email) {
        var re = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
        return re.test(String(email).toLowerCase());
    }

    screens.ClientListScreenWidget.include({
        save_client_details: function(partner) {
            var self = this;
            var email = this.$('.client-details-contents input[name="email"]').val();

            if (email && !validateEmail(email)) {
                self.gui.show_popup('error', {
                    'title': 'Invalid Email',
                    'body': 'Please enter a valid email address.',
                });
                return;
            }

            this._super(partner);
        }
    });
});
