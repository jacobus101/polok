odoo.define('pos_map_tax_fiscal_position.pos_map_tax_fiscal_position', function(require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.Ordeline.extend({
        _map_tax_fiscal_position: function(tax) {
            var self = this;
            var current_order = this.pos.get_order();
            var order_fiscal_position = current_order && current_order.fiscal_position;
            var taxes = [];
    
            if (order_fiscal_position) {
                var tax_mappings = _.filter(order_fiscal_position.fiscal_position_taxes_by_id, function (fiscal_position_tax) {
                    return fiscal_position_tax.tax_src_id[0] === tax.id;
                });
    
                if (tax_mappings && tax_mappings.length) {
                    _.each(tax_mappings, function(tm) {
                        if (tm.tax_dest_id) {
                            taxes.push(self.pos.taxes_by_id[tm.tax_dest_id[0]]);
                        }
                    });
                } else{
                    taxes.push(tax);
                }
            } else {
                taxes.push(tax);
            }
    
            return taxes;
        },
    });
});