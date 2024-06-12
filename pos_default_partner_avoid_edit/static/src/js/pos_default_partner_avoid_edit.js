// static/src/js/pos_default_partner_avoid_edit.js
odoo.define('pos_default_partner_avoid_edit.disable_edit_button', function(require) {
    'use strict';

    var PosComponent = require('point_of_sale.PosComponent');
    var Registries = require('point_of_sale.Registries');

    const DisableEditButton = (PosComponent) => class extends PosComponent {
        constructor() {
            super(...arguments);
            this.env.pos.on('change:selectedClient', this, this._checkDefaultPartner);
        }

        async willStart() {
            await super.willStart();
            this._checkDefaultPartner();
        }

        _checkDefaultPartner() {
            const defaultPartner = this.env.pos.db.get_partner_by_id(this.env.pos.config.default_partner_id);
            const currentPartner = this.env.pos.get_order().get_client();
            const editButton = document.querySelector('.button.edit');

            if (defaultPartner && currentPartner && defaultPartner.id === currentPartner.id) {
                if (editButton) {
                    editButton.style.display = 'none';
                }
            } else {
                if (editButton) {
                    editButton.style.display = '';
                }
            }
        }
    };

    Registries.Component.extend(PosComponent, DisableEditButton);

    return PosComponent;
});
