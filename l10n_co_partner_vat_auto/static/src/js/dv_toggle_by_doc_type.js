odoo.define('l10n_co_partner_vat_auto.dv_toggle_by_doc_type', function (require) {
    "use strict";

    const screens = require('point_of_sale.screens');

    screens.ClientListScreenWidget.include({
        display_client_details: function(visibility, partner, clickpos) {
            this._super(visibility, partner, clickpos);

            if (visibility !== 'edit') { return; }

            const $docType = this.$('select[name="l10n_co_document_type"]');
            const $dvContainer = this.$('.check-digit-container');

            function toggleDVField() {
                const selected = $docType.val();
                if (selected === 'rut') {
                    $dvContainer.show();
                } else {
                    $dvContainer.hide();
                }
            }

            // Ejecutar al cargar
            toggleDVField();

            // Ejecutar cuando el usuario cambia el tipo de documento
            $docType.off('change.dvToggle').on('change.dvToggle', toggleDVField);
        }
    });
});
