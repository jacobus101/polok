odoo.define('l10n_co_partner_vat_auto.set_default_country', function (require) {
    'use strict';

    const screens = require('point_of_sale.screens');

    screens.ClientListScreenWidget.include({
        display_client_details: function (visibility, partner, clickpos) {
            this._super(visibility, partner, clickpos);

            if (visibility !== 'edit') return;

            const colCountry = this.pos.countries?.find(c => c.name === 'Colombia');
            if (!colCountry) return;

            const $countrySelect = this.$('.client-address-country');
            $countrySelect.val(colCountry.id);
            $countrySelect.attr('disabled', true);

            // --- Establecer Departamento por defecto
            const defaultDepartment = this.pos.states?.find(d => d.name.includes('D.C.'));
            const $departmentSelect = this.$('select[name="state_id"]');
            if (defaultDepartment && !partner.state_id) {
                $departmentSelect.val(defaultDepartment.id);
            }

            // --- Establecer régimen por defecto
            const defaultRegime = this.pos.type_regimes?.find(r => r.name.includes('No responsable'));
            const $regimeSelect = this.$('select[name="type_regime_id"]');
            if (defaultRegime && !partner.type_regime_id) {
                $regimeSelect.val(defaultRegime.id);
            }

            // --- Responsabilidad: No aplica ---
            const defaultLiability = this.pos.type_liabilities?.find(l => l.name.toLowerCase().includes('no aplica'));
            if (defaultLiability && !partner.type_liability_id) {
                this.$('select[name="type_liability_id"]').val(defaultLiability.id);
            }

            // --- Municipio: Bogotá ---
            const defaultMunicipality = this.pos.municipalities?.find(m => m.name.includes('Bogotá'));
            if (defaultMunicipality && !partner.municipality_id) {
                this.$('select[name="municipality_id"]').val(defaultMunicipality.id);
            }
        }
    });
});
