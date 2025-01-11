odoo.define('pos_geolocation.pos_geolocation', function (require) {
    'use strict';

    const models = require('point_of_sale.models');

    // Extend the POS Order model to include geolocation
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

        set_geolocation: function () {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition((position) => {
                    this.latitude = position.coords.latitude;
                    this.longitude = position.coords.longitude;
                    console.log('Geolocation captured:', this.latitude, this.longitude);
                }, (error) => {
                    console.error('Error capturing geolocation:', error.message);
                });
            } else {
                console.warn('Geolocation is not supported by this browser.');
            }
        }
    });

    // Trigger geolocation before pushing an order to the backend
    const PosModel = models.PosModel;
    models.PosModel = PosModel.extend({
        push_order: function (order, opts) {
            order.set_geolocation(); // Capture geolocation
            return this._super(order, opts);
        }
    });
});
