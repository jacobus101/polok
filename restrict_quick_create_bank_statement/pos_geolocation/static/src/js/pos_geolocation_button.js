odoo.define('pos_geolocation.pos_geolocation_button', function (require) {
    'use strict';

    const screens = require('point_of_sale.screens');
    const gui = require('point_of_sale.gui');
    const core = require('web.core');

    const _t = core._t;

    // Define a new button for capturing geolocation
    const GeolocationButton = screens.ActionButtonWidget.extend({
        template: 'GeolocationButton',
        button_click: function () {
            const order = this.pos.get_order();
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        order.latitude = position.coords.latitude;
                        order.longitude = position.coords.longitude;
                        this.gui.show_popup('confirm', {
                            title: _t('Geolocation Captured'),
                            body: _t(`Latitude: ${order.latitude}, Longitude: ${order.longitude}`),
                        });
                    },
                    (error) => {
                        this.gui.show_popup('error', {
                            title: _t('Geolocation Error'),
                            body: _t('Unable to capture geolocation: ' + error.message),
                        });
                    }
                );
            } else {
                this.gui.show_popup('error', {
                    title: _t('Geolocation Not Supported'),
                    body: _t('Your browser does not support geolocation.'),
                });
            }
        },
    });

    // Add the button to the POS screens
    screens.define_action_button({
        name: 'geolocation_button',
        widget: GeolocationButton,
        condition: function () {
            return true; // Always show the button
        },
    });
});
