odoo.define('pos_auto_invoice.pos_auto_invoice', function (require) {
    "use strict";

    var gui = require('point_of_sale.gui');
    var screens = require('point_of_sale.screens');

    screens.PaymentScreenWidget.include({
        show: function() {
            var self = this;
            this._super();
            var pos_order = this.pos.get_order();

            if (this.pos.config.invoice_type_setting === 'pos_invoice' && this.pos.config.module_account) {
                if (pos_order !== null) {
                    pos_order.set_to_invoice(true);
                    this.$('.js_invoice').addClass('highlight');
                    this.$('.js_electronic_invoice').removeClass('hidden');
                }
            }

            if (this.pos.config.invoice_type_setting === 'electronic_invoice' && this.pos.config.module_account) {
                if (pos_order !== null) {
                    pos_order.set_to_electronic_invoice(true);
                    this.$('.js_electronic_invoice').addClass('highlight');
                    this.$('.js_invoice').addClass('highlight');
                    this.$('.js_electronic_invoice').removeClass('hidden');
                }
            }

            if (this.pos.config.invoice_type_setting === 'hide_invoice') {
                this.$('.js_invoice').addClass('hidden');
                this.$('.js_electronic_invoice').addClass('hidden');
            }
        }
    });
});
