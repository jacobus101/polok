odoo.define('l10n_co_partner_vat_auto.dv_utils', function (require) {
    'use strict';

    /**
     * Calcula el dígito de verificación para un NIT colombiano.
     * @param {String} nit – Solo dígitos, sin puntos ni guiones.
     * @return {String} dígito (0-9).
     */
    function computeDV(nit) {
        nit = (nit || '').replace(/[^0-9]/g, '');
        if (nit.length < 4) { return ''; }

        var primes = [3,7,13,17,19,23,29,37,41,43,47,53,59,67,71];
        var sum = 0;
        for (var i = 0; i < nit.length; i++) {
            var idx = nit.length - 1 - i;
            sum += parseInt(nit.charAt(idx), 10) * primes[i];
        }
        var mod = sum % 11;
        return (mod > 1 ? 11 - mod : mod).toString();
    }

    return computeDV;
});
