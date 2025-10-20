/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import PartnerDetailsEdit from 'point_of_sale.PartnerDetailsEdit';

console.log('🚀 MÓDULO pos_vat_blocker - Cargando validación de cliente...');

// Función para validar formato de email
const isValidEmail = (email) => {
    if (!email || email.trim() === '') return false;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(email.trim());
    console.log('🔍 Validando email:', email, '-> Resultado:', isValid);
    return isValid;
};

// Extensión del PartnerDetailsEdit para validar al guardar cliente
const MyPartnerDetailsEdit = (PartnerDetailsEdit) => class extends PartnerDetailsEdit {
    async saveChanges() {
        console.log('🚨 INTERCEPTANDO GUARDADO DE CLIENTE - pos_vat_blocker');
        
        // Obtener los datos del cliente desde el formulario
        // En PartnerDetailsEdit, los datos están en this.changes
        const partner = this.changes || {};
        console.log('🔍 Cliente a guardar:', partner);
        console.log('🔍 Cambios del formulario:', this.changes);
        
        // Si no hay cambios, continuar con el flujo normal
        if (!partner || Object.keys(partner).length === 0) {
            console.log('⚠️ NO HAY CAMBIOS - Continuando con flujo normal');
            return super.saveChanges();
        }
        
        // Validaciones del cliente
        const validations = [];
        
        console.log('🔍 Validando cliente:');
        console.log('  - VAT:', partner.vat);
        console.log('  - Email:', partner.email);
        console.log('  - Email válido:', partner.email ? isValidEmail(partner.email) : 'No hay email');
        
        // Validación 1: Cliente debe tener VAT/NIT
        if (!partner.vat || partner.vat.trim() === '') {
            validations.push("• Completa el campo NIT/VAT del cliente");
        }
        
        // Validación 2: Cliente debe tener email válido
        if (!partner.email || partner.email.trim() === '') {
            validations.push("• Completa el campo Email con formato válido (ejemplo@dominio.com)");
        } else if (!isValidEmail(partner.email)) {
            validations.push("• El formato del Email no es válido (ejemplo@dominio.com)");
        }
        
        console.log('🔍 Validaciones encontradas:', validations);
        
        // Si hay errores de validación, bloquear
        if (validations.length > 0) {
            console.log('❌ BLOQUEANDO GUARDADO - Errores encontrados:', validations);
            
            // Mostrar popup de error compacto
            this.showPopup('ErrorPopup', {
                title: '⚠️ Datos del Cliente Incompletos',
                body: `Para guardar el cliente:\n\n${validations.join('\n')}`,
            });
            
            console.log('🛑 GUARDADO BLOQUEADO - No se procede con el guardado');
            return; // <- Bloquea la acción de guardado
        }

        console.log('✅ CLIENTE VÁLIDO - Procediendo con el guardado normal');
        
        // Continúa con el flujo normal llamando al método padre
        return super.saveChanges();
    }
};

// Registrar la extensión usando el método de Odoo 16
Registries.Component.extend(PartnerDetailsEdit, MyPartnerDetailsEdit);

console.log('✅ Extensión de PartnerDetailsEdit registrada correctamente - pos_vat_blocker listo para validar clientes');
