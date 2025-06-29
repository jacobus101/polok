odoo.define('l10n_co_partner_vat_auto.pos_partner_vat', function (require) {
    'use strict';

    //----------------------------------------------------------------------
    //  DEPENDENCIAS
    //----------------------------------------------------------------------
    const screens = require('point_of_sale.screens');
    const core    = require('web.core');
    const _t      = core._t;

    //----------------------------------------------------------------------
    //  UTILIDADES
    //----------------------------------------------------------------------
    /** Calcula el dígito de verificación para un NIT colombiano */
    function computeDV(nit) {
        nit = (nit || '').replace(/[^0-9]/g, '');
        if (nit.length < 4) { return ''; }

        const primes = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71];
        let sum = 0;
        for (let i = 0; i < nit.length; i++) {
            const idx = nit.length - 1 - i;
            sum += parseInt(nit.charAt(idx), 10) * primes[i];
        }
        const mod = sum % 11;
        return (mod > 1 ? 11 - mod : mod).toString();
    }

    /** Arma el VAT final usando el DV que escribió el usuario (ya validado) */
    function computeVAT(partner) {
        const country = 'CO'
        const docType = partner.type_document_identification_id ?
                        partner.type_document_identification_id[1] : null;
        const nit = partner.identification_document || '';

        if (!nit) { return ''; }

        if (docType === 'NIT') {                       // NIT
            return country + nit + (partner.check_digit || '');
        } else if (docType === '43') {                // Ejemplo: tipo 43
            return 'CO' + nit;
        }
        return country + nit;                         // CC, CE, etc.
    }

    //----------------------------------------------------------------------
    //  PARCHE A LA PANTALLA DE CLIENTES
    //----------------------------------------------------------------------
    screens.ClientListScreenWidget.include({

        display_client_details: function (visibility, partner, clickpos) {
            this._super(visibility, partner, clickpos);
            if (visibility !== 'edit') { return; }

            // validación “en vivo” del DV ─ sin cambios
            const $nit = this.$('input.detail[name="identification_document"]');
            const $dv  = this.$('input.detail[name="check_digit"]');
            $dv.off('blur.dv').on('blur.dv', () => {
                const expected = computeDV($nit.val());
                if (expected && expected !== $dv.val()) {
                    this.gui.show_popup('error', {
                        title: _t('Dígito incorrecto'),
                        body:  _t('Para este NIT el dígito de verificación debería ser ') + expected + '.',
                    });
                    $dv.css('border-color', 'red');
                } else {
                    $dv.css('border-color', '');
                }
            });
        },

        // ← ¡UNA sola función!
        save_client_details: function (partner) {

            // -------- generar VAT y añadirlo al dict ----
            partner.vat = computeVAT(partner);

            return this._super(partner);   // guarda en el servidor
        },
    });
});
