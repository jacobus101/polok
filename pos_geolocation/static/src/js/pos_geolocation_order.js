odoo.define('pos_geolocation.pos_geolocation_order', function (require) {
    'use strict';

    const models = require('point_of_sale.models');

    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            this.latitude = null;
            this.longitude = null;
            this._super(attributes, options);
        },
        export_as_JSON: function () {
            const data = this._super();
            data.latitude = this.latitude;
            data.longitude = this.longitude;
            return data;
        },
    });
});
