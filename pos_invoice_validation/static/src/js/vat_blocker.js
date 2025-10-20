/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import PaymentScreen from 'point_of_sale.PaymentScreen';

console.log('🚀 MÓDULO pos_vat_blocker CARGADO - Inicializando para Odoo 16...');

// Extensión del PaymentScreen usando el método de Odoo 16
const MyPaymentScreen = (PaymentScreen) => class extends PaymentScreen {
    async validateOrder(isForceValidate) {
        console.log('🚨 INTERCEPTANDO VALIDACIÓN DE ORDEN - pos_vat_blocker');
        console.log('🔍 Parámetros recibidos:', { isForceValidate });
        
        // Obtiene el pedido activo y su partner
        const pos = this.env?.pos || this.pos;
        console.log('🔍 POS object:', pos);
        
        const order = pos && pos.get_order ? pos.get_order() : null;
        console.log('🔍 Order object:', order);
        
        const partner = order && (order.get_partner?.() || order.partner || null);
        console.log('🔍 Partner object:', partner);
        
        const partnerName = partner && (partner.name || "Cliente");
        console.log('🔍 Partner name:', partnerName);
        
        // Log detallado de los datos del cliente
        if (partner) {
            console.log('📋 DATOS COMPLETOS DEL CLIENTE:');
            console.log('  - ID:', partner.id);
            console.log('  - Nombre:', partner.name);
            console.log('  - Email:', partner.email);
            console.log('  - VAT:', partner.vat);
            console.log('  - Teléfono:', partner.phone);
            console.log('  - Es empresa:', partner.is_company);
            console.log('  - Todos los campos:', partner);
        } else {
            console.log('⚠️ NO HAY CLIENTE SELECCIONADO');
        }

        // Función para validar formato de email
        const isValidEmail = (email) => {
            if (!email || email.trim() === '') return false;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email.trim());
        };

        // Validaciones del cliente
        const validations = [];
        
        // Validación 1: Cliente debe existir
        if (!partner) {
            validations.push("• Selecciona un cliente antes de validar");
        } else {
            // Validación 2: Cliente debe tener VAT/NIT
            if (!partner.vat) {
                validations.push("• Completa el campo NIT/VAT del cliente");
            }
            
            // Validación 3: Cliente debe tener email válido
            if (!partner.email || !isValidEmail(partner.email)) {
                validations.push("• Completa el campo Email con formato válido (ejemplo@dominio.com)");
            }
        }

        // Validación 4: Verificar líneas de orden
        if (order && order.get_orderlines) {
            const orderlines = order.get_orderlines();
            console.log('🔍 Líneas de orden encontradas:', orderlines.length);
            
            const invalidLines = orderlines.filter(line => {
                // Usar los métodos correctos para Odoo 16
                const quantity = line.get_quantity ? line.get_quantity() : (line.quantity || 0);
                const price = line.get_unit_price ? line.get_unit_price() : (line.price_unit || 0);
                
                console.log('🔍 Línea:', {
                    quantity: quantity,
                    price: price,
                    product: line.product ? line.product.display_name : 'Sin producto'
                });
                
                const isInvalid = !quantity || quantity <= 0 || !price || price <= 0;
                if (isInvalid) {
                    console.log('❌ Línea inválida detectada:', { quantity, price });
                }
                
                return isInvalid;
            });
            
            console.log('🔍 Líneas inválidas encontradas:', invalidLines.length);
            
            if (invalidLines.length > 0) {
                validations.push("• Revisa las líneas de orden: cantidad y precio deben ser mayores a 0");
            }
        }

        // Si hay errores de validación, bloquear
        if (validations.length > 0) {
            console.log('❌ BLOQUEANDO VALIDACIÓN - Errores encontrados:', validations);
            
            // Mostrar popup de error compacto
            this.showPopup('ErrorPopup', {
                title: '⚠️ Datos Incompletos',
                body: `Para continuar con la validación:\n\n${validations.join('\n')}`,
            });
            
            console.log('🛑 VALIDACIÓN BLOQUEADA - No se procede con el pago');
            return; // <- Bloquea la acción de validación
        }

        console.log('✅ CLIENTE VÁLIDO - Procediendo con la validación normal');
        
        // Continúa con el flujo normal llamando al método padre
        return super.validateOrder(isForceValidate);
    }
};

// Registrar la extensión usando el método de Odoo 16
Registries.Component.extend(PaymentScreen, MyPaymentScreen);

console.log('✅ Extensión registrada correctamente - pos_vat_blocker listo para interceptar validaciones');
