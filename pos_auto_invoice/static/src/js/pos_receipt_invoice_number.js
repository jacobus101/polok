odoo.define('pos_receipt_invoice_number', function (require) {
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var qweb = core.qweb;

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            _super_Order.initialize.apply(this, arguments);
            if (this.pos.config.pos_auto_invoice) {
                this.to_invoice = true;
            }
        },
        init_from_JSON: function (json) {
            var res = _super_Order.init_from_JSON.apply(this, arguments);
            if (json.to_invoice) {
                this.to_invoice = json.to_invoice;
            }
        }
    });
});
