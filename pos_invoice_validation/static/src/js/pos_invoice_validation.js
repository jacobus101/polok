/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

/**
 * Función para validar formato de email (obligatorio para facturación electrónica)
 * @param {string} email - Email a validar
 * @returns {Object} - {valid: boolean, message: string}
 */
function validateEmail(email) {
    if (!email || email.trim() === '') {
        return { 
            valid: false, 
            message: _t('El correo electrónico es obligatorio para facturación electrónica.') 
        };
    }
    
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
        return { 
            valid: false, 
            message: _t('El formato del correo electrónico no es válido. Por favor, ingrese un email válido (ejemplo: usuario@dominio.com).') 
        };
    }
    
    return { valid: true, message: '' };
}

/**
 * Función para validar NIT/Documento de identidad (obligatorio para DIAN)
 * @param {string} vat - NIT/Documento a validar
 * @returns {Object} - {valid: boolean, message: string}
 */
function validateVat(vat) {
    if (!vat || vat.trim() === '') {
        return { 
            valid: false, 
            message: _t('El NIT/Documento de identidad es obligatorio para facturación electrónica (DIAN).') 
        };
    }
    
    // Validar formato básico de NIT colombiano
    const vatRegex = /^[0-9]{6,15}$/;
    if (!vatRegex.test(vat.replace(/[^0-9]/g, ''))) {
        return { 
            valid: false, 
            message: _t('El formato del NIT/Documento no es válido. Debe contener entre 6 y 15 dígitos.') 
        };
    }
    
    return { valid: true, message: '' };
}

/**
 * Función para validar campos obligatorios del cliente según configuración
 * @param {Object} partner - Objeto del cliente
 * @param {Object} config - Configuración de validación
 * @returns {Object} - {valid: boolean, message: string}
 */
function validateRequiredFields(partner, config) {
    const validationErrors = [];
    
    // Validar email si está habilitado
    if (config.require_email) {
        const emailValidation = validateEmail(partner.email);
        if (!emailValidation.valid) {
            validationErrors.push(emailValidation.message);
        }
    }
    
    // Validar NIT/Documento si está habilitado
    if (config.require_vat) {
        const vatValidation = validateVat(partner.vat);
        if (!vatValidation.valid) {
            validationErrors.push(vatValidation.message);
        }
    }
    
    // Validar tipo de identificación si está habilitado (obligatorio para DIAN)
    if (config.require_identification_type && (!partner.l10n_latam_identification_type_id)) {
        validationErrors.push(_t('El tipo de identificación es obligatorio para facturación electrónica (DIAN).'));
    }
    
    // Validar régimen fiscal si está habilitado (obligatorio para DIAN)
    if (config.require_regime && (partner.type_regime_id === undefined || partner.type_regime_id === null)) {
        validationErrors.push(_t('El régimen fiscal es obligatorio para facturación electrónica (DIAN).'));
    }
    
    // Validar responsabilidad fiscal si está habilitado (obligatorio para DIAN)
    if (config.require_liability && (partner.type_liability_id === undefined || partner.type_liability_id === null)) {
        validationErrors.push(_t('La responsabilidad fiscal es obligatoria para facturación electrónica (DIAN).'));
    }
    
    // Validar municipio si está habilitado (obligatorio para DIAN)
    if (config.require_municipality && (partner.municipality_id === undefined || partner.municipality_id === null)) {
        validationErrors.push(_t('El municipio es obligatorio para facturación electrónica (DIAN).'));
    }
    
    if (validationErrors.length > 0) {
        return { 
            valid: false, 
            message: validationErrors.join('; ') 
        };
    }
    
    return { valid: true, message: '' };
}

/**
 * Función para obtener configuración de validación (versión simplificada)
 * @returns {Object} - Configuración de validación
 */
function getValidationConfig() {
    // Usar configuración local por defecto para evitar problemas de autenticación
    console.log('🔧 Usando configuración local de validación');
        return {
            require_email: true,
            require_vat: true,
            require_identification_type: true,
            require_regime: true,
            require_liability: true,
            require_municipality: true
        };
}

/**
 * Función para mostrar mensaje de error estándar de Odoo
 * @param {string} message - Mensaje a mostrar
 */
function showErrorMessage(message) {
    // Usar el sistema de notificaciones de Odoo si está disponible
    if (window.odoo && window.odoo.__WOWL_DEBUG__ && window.odoo.__WOWL_DEBUG__.services && window.odoo.__WOWL_DEBUG__.services.notification) {
        window.odoo.__WOWL_DEBUG__.services.notification.add(message, { 
            type: 'danger',
            sticky: true,
            title: _t('Error de Validación')
        });
    } else {
        // Fallback a alert nativo
        alert(message);
    }
}

/**
 * Función para mostrar mensaje de éxito
 * @param {string} message - Mensaje a mostrar
 */
function showSuccessMessage(message) {
    // Usar el sistema de notificaciones de Odoo si está disponible
    if (window.odoo && window.odoo.__WOWL_DEBUG__ && window.odoo.__WOWL_DEBUG__.services && window.odoo.__WOWL_DEBUG__.services.notification) {
        window.odoo.__WOWL_DEBUG__.services.notification.add(message, { 
            type: 'success',
            sticky: false,
            title: _t('Validación Exitosa')
        });
    } else {
        // Fallback a alert nativo
        alert(message);
    }
}


/**
 * Función para extraer email del texto del cliente
 * @param {string} text - Texto del cliente
 * @returns {string} - Email encontrado
 */
function extractEmailFromText(text) {
    const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
    const matches = text.match(emailRegex);
    return matches && matches.length > 0 ? matches[0] : '';
}

// ============================================================================
// CONFIGURACIÓN GLOBAL
// ============================================================================

// Variable global para almacenar la configuración
let validationConfig = null;

document.addEventListener('DOMContentLoaded', function() {
    // Obtener configuración de validación
    validationConfig = getValidationConfig();
    console.log('🔧 POS Invoice Validation: Configuración cargada:', validationConfig);
});

// ============================================================================
// VALIDACIÓN FINAL EN PANTALLA DE PAGO
// ============================================================================

// Nueva estrategia: Interceptar todos los clics y detectar contexto de pago
function setupValidationInterception() {
    console.log('🔧 Configurando interceptación global de clics...');
    
    // Obtener configuración de validación
    const config = getValidationConfig();
    console.log('🔧 Configuración de validación:', config);
    
    // Función para detectar si estamos en pantalla de pago
    function isPaymentScreen() {
        const paymentIndicators = [
            '.payment-screen',
            '.payment-methods',
            '.payment-buttons',
            '[data-screen="payment"]',
            '.pos-payment-screen'
        ];
        
        return paymentIndicators.some(selector => document.querySelector(selector));
    }
    
    // Función para detectar si el clic es en un elemento de validación/pago
    function isValidationClick(target) {
        // Buscar el elemento clickeable más cercano (button, div, span, etc.)
        const clickableElement = target.closest('button, div, span, a, [role="button"]');
        if (!clickableElement) return false;
        
        const text = clickableElement.textContent?.toLowerCase() || '';
        const title = clickableElement.title?.toLowerCase() || '';
        const classes = clickableElement.className?.toLowerCase() || '';
        const id = clickableElement.id?.toLowerCase() || '';
        const tagName = clickableElement.tagName?.toLowerCase() || '';
        
        console.log('🔍 Analizando elemento clickeable:', {
            tagName: tagName,
            text: text,
            title: title,
            classes: classes,
            id: id
        });
        
        // EXCLUIR elementos que NO son de validación
        const excludedClasses = [
            'payment-name', 'payment-method', 'payment-option',
            'cash', 'bank', 'credit', 'debit', 'method',
            'option', 'choice', 'select', 'picker'
        ];
        
        const isExcluded = excludedClasses.some(excludedClass => 
            classes.includes(excludedClass) || 
            text.includes(excludedClass) ||
            id.includes(excludedClass)
        );
        
        if (isExcluded) {
            console.log('❌ Elemento excluido (método de pago):', excludedClasses.find(excludedClass => 
                classes.includes(excludedClass) || text.includes(excludedClass) || id.includes(excludedClass)
            ));
            return false;
        }
        
        // Solo detectar elementos que claramente son de validación
        const validationKeywords = [
            'validate', 'validar', 'confirm', 'confirmar', 
            'process', 'procesar', 'submit', 'enviar',
            'finish', 'terminar', 'complete', 'completar',
            'checkout', 'finalizar', 'done', 'hecho'
        ];
        
        const isValidation = validationKeywords.some(keyword => 
            text.includes(keyword) || 
            title.includes(keyword) || 
            classes.includes(keyword) || 
            id.includes(keyword)
        );
        
        // Detectar elementos con clases específicas de validación (más restrictivo)
        const hasValidationClass = (classes.includes('validation') && classes.includes('highlight')) || 
                                 (classes.includes('submit') && classes.includes('primary')) ||
                                 (classes.includes('button') && classes.includes('next') && classes.includes('validation'));
        
        // Detectar elementos que están en áreas específicas de validación
        const isInValidationArea = clickableElement.closest('.validation-buttons, .checkout-buttons, .submit-area');
        
           // Aceptar botones reales, elementos con role="button", o elementos con clases específicas de validación
           const isRealButton = tagName === 'button' || 
                               clickableElement.getAttribute('role') === 'button' ||
                               (classes.includes('button') && classes.includes('validation'));
           
           const result = (isValidation || hasValidationClass || isInValidationArea) && isRealButton;
        
        console.log('🎯 Resultado de detección:', {
            isValidation: isValidation,
            hasValidationClass: hasValidationClass,
            isInValidationArea: !!isInValidationArea,
            isRealButton: isRealButton,
            finalResult: result
        });
        
        return result;
    }
    
    // Función para obtener datos del cliente
    function getCustomerData() {
        console.log('🔍 NUEVA ESTRATEGIA: Buscando objeto order en Odoo POS...');
        
        // Estrategia 1: Acceder al objeto order desde el estado de Odoo POS
        try {
            // Buscar la aplicación POS en el DOM
            const posApp = document.querySelector('[data-pos-app], .pos-app, #pos-app');
            if (posApp && posApp.__owl__) {
                console.log('🔍 Aplicación POS encontrada:', posApp);
                const posState = posApp.__owl__.state;
                console.log('🔍 Estado de POS:', posState);
                
                if (posState && posState.order) {
                    console.log('🔍 Objeto order encontrado:', posState.order);
                    if (posState.order.partner) {
                        console.log('📋 Cliente desde order.partner:', posState.order.partner);
                        return posState.order.partner;
                    }
                }
            }
        } catch (e) {
            console.log('⚠️ Error accediendo al estado de POS:', e);
        }
        
        // Estrategia 2: Buscar en el contexto global de Odoo
        try {
            if (window.odoo && window.odoo.__WOWL_DEBUG__ && window.odoo.__WOWL_DEBUG__.services && window.odoo.__WOWL_DEBUG__.services.pos) {
                const order = window.odoo.__WOWL_DEBUG__.services.pos.get_order();
                if (order && order.partner) {
                    console.log('📋 Cliente obtenido desde servicios Odoo:', order.partner);
                    return order.partner;
                }
            }
        } catch (e) {
            console.log('⚠️ No se pudo obtener cliente desde servicios Odoo');
        }
        
        // Estrategia 3: Buscar en el contexto de la aplicación
        try {
            // Buscar en el contexto global
            const posContext = window.odoo?.pos || window.pos || window.POS;
            if (posContext) {
                console.log('🔍 Contexto POS encontrado:', posContext);
                if (posContext.order && posContext.order.partner) {
                    console.log('📋 Cliente desde contexto POS:', posContext.order.partner);
                    return posContext.order.partner;
                }
            }
        } catch (e) {
            console.log('⚠️ Error accediendo al contexto POS:', e);
        }
        
        // Estrategia 4: Buscar el objeto order en diferentes ubicaciones del DOM
        try {
            console.log('🔍 Buscando objeto order en elementos del DOM...');
            
            // Buscar en elementos que puedan contener el estado de la aplicación
            const possibleContainers = document.querySelectorAll('[data-pos], [data-order], .pos-container, .order-container, [class*="pos-"], [class*="order-"]');
            
            for (const container of possibleContainers) {
                console.log('🔍 Inspeccionando contenedor:', container);
                
                // Buscar propiedades que puedan contener el order
                if (container.__owl__ && container.__owl__.state && container.__owl__.state.order) {
                    console.log('🔍 Order encontrado en contenedor:', container.__owl__.state.order);
                    if (container.__owl__.state.order.partner) {
                        console.log('📋 Cliente desde contenedor:', container.__owl__.state.order.partner);
                        return container.__owl__.state.order.partner;
                    }
                }
                
                // Buscar en propiedades del elemento
                if (container.order && container.order.partner) {
                    console.log('📋 Cliente desde propiedad order:', container.order.partner);
                    return container.order.partner;
                }
            }
        } catch (e) {
            console.log('⚠️ Error buscando order en contenedores:', e);
        }
        
        // Estrategia 5: Buscar en el contexto de React/Vue si está disponible
        try {
            console.log('🔍 Buscando en contexto de frameworks...');
            
            // Buscar en el contexto de React
            if (window.React && window.React.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED) {
                console.log('🔍 React encontrado, buscando estado...');
                // Aquí podríamos buscar en el estado de React si es necesario
            }
            
            // Buscar en el contexto de Vue
            if (window.Vue) {
                console.log('🔍 Vue encontrado, buscando estado...');
                // Aquí podríamos buscar en el estado de Vue si es necesario
            }
        } catch (e) {
            console.log('⚠️ Error buscando en frameworks:', e);
        }
        
        // Fallback: Buscar en el DOM con múltiples estrategias
        console.log('🔍 Fallback: Buscando cliente en DOM...');
        
        // Estrategia 1: Buscar en elementos de cliente específicos del POS
        const customerSelectors = [
            '.customer-field', '.partner-field', '[data-partner-id]', 
            '.partner-name', '.customer-name', '.customer-info',
            '.pos-customer', '.pos-partner', '.orderline-partner',
            '.partner-line', '.customer-line', '.partner-info',
            '.customer-details', '.partner-details'
        ];
        
        for (const selector of customerSelectors) {
            const elements = document.querySelectorAll(selector);
            console.log(`🔍 Buscando con selector "${selector}": ${elements.length} elementos encontrados`);
            
            for (const field of elements) {
                const text = field.textContent?.trim() || '';
                console.log(`🔍 Elemento encontrado: "${text}"`);
                
                if (text && !text.includes('Walk-in') && !text.includes('Customer') && text.length > 2) {
                    console.log('📋 Cliente encontrado en DOM:', text);
                    return {
                        name: text,
                        email: field.querySelector('[data-email]')?.getAttribute('data-email') || 
                               field.querySelector('.email')?.textContent?.trim() || '',
                        vat: field.querySelector('[data-vat]')?.getAttribute('data-vat') || 
                             field.querySelector('.vat')?.textContent?.trim() || '',
                        l10n_latam_identification_type_id: field.querySelector('[data-l10n-latam-identification-type-id]')?.getAttribute('data-l10n-latam-identification-type-id') || null,
                        type_regime_id: field.querySelector('[data-type-regime-id]')?.getAttribute('data-type-regime-id') || null,
                        type_liability_id: field.querySelector('[data-type-liability-id]')?.getAttribute('data-type-liability-id') || null,
                        municipality_id: field.querySelector('[data-municipality-id]')?.getAttribute('data-municipality-id') || null
                    };
                }
            }
        }
        
        // Estrategia 2: Buscar en áreas específicas del POS donde aparece el cliente
        console.log('🔍 Buscando en áreas específicas del POS...');
        
        // Buscar en el área de resumen de la orden (lado derecho)
        const orderSummary = document.querySelector('.order-summary, .pos-order-summary, .order-details, .pos-order-details');
        if (orderSummary) {
            console.log('🔍 Buscando en resumen de orden...');
            const customerElements = orderSummary.querySelectorAll('.customer, .partner, .client, [data-customer], [data-partner]');
            for (const element of customerElements) {
                const text = element.textContent?.trim() || '';
                if (text && text.length > 2 && !text.includes('Customer') && !text.includes('Account')) {
                    console.log('📋 Cliente encontrado en resumen de orden:', text);
                    return {
                        name: text,
                        email: '',
                        vat: '',
                        l10n_latam_identification_type_id: null,
                        type_regime_id: null,
                        type_liability_id: null,
                        municipality_id: null
                    };
                }
            }
        }
        
        // Buscar en el área de información del cliente
        const customerInfo = document.querySelector('.customer-info, .partner-info, .client-info, .pos-customer-info');
        if (customerInfo) {
            console.log('🔍 Buscando en información del cliente...');
            const nameElement = customerInfo.querySelector('.name, .customer-name, .partner-name, .client-name');
            if (nameElement) {
                const text = nameElement.textContent?.trim() || '';
                if (text && text.length > 2) {
                    console.log('📋 Cliente encontrado en información:', text);
                    return {
                        name: text,
                        email: '',
                        vat: '',
                        l10n_latam_identification_type_id: null,
                        type_regime_id: null,
                        type_liability_id: null,
                        municipality_id: null
                    };
                }
            }
        }
        
        // Buscar en elementos con atributos específicos del cliente
        const customerElements = document.querySelectorAll('[data-customer-name], [data-partner-name], [data-client-name]');
        for (const element of customerElements) {
            const text = element.textContent?.trim() || element.getAttribute('data-customer-name') || 
                        element.getAttribute('data-partner-name') || element.getAttribute('data-client-name');
            if (text && text.length > 2) {
                console.log('📋 Cliente encontrado por atributos:', text);
                return {
                    name: text,
                    email: '',
                    vat: '',
                    l10n_latam_identification_type_id: null,
                    type_regime_id: null,
                    type_liability_id: null,
                    municipality_id: null
                };
            }
        }
        
        // Estrategia 3: Buscar en el área de la orden actual
        console.log('🔍 Buscando en área de orden actual...');
        const orderArea = document.querySelector('.order-area, .pos-order-area, .current-order, .pos-current-order');
        if (orderArea) {
            const customerElements = orderArea.querySelectorAll('*');
            for (const element of customerElements) {
                const text = element.textContent?.trim() || '';
                // Buscar texto que parezca nombre de cliente (no botones, no palabras técnicas)
                if (text && 
                    text.length > 3 && 
                    text.length < 50 && 
                    !text.includes('€') && 
                    !text.includes('Payment') && 
                    !text.includes('Cash') && 
                    !text.includes('Bank') && 
                    !text.includes('Validate') &&
                    !text.includes('Back') &&
                    !text.includes('Total') &&
                    !text.includes('Change') &&
                    !text.includes('Remaining') &&
                    !text.includes('Walk-in') &&
                    !text.includes('Customer') &&
                    !text.includes('Account') &&
                    !text.match(/^\d+$/) && // No solo números
                    !text.match(/^[A-Z\s]+$/) && // No solo mayúsculas (botones)
                    element.children.length === 0) { // Solo elementos hoja
                    
                    console.log('📋 Cliente encontrado en área de orden:', text);
                    return {
                        name: text,
                        email: '',
                        vat: '',
                        l10n_latam_identification_type_id: null,
                        type_regime_id: null,
                        type_liability_id: null,
                        municipality_id: null
                    };
                }
            }
        }
        
        // Estrategia 4: Inspección completa del DOM para debug
        console.log('🔍 ESTRATEGIA DE DEBUG: Inspeccionando todo el DOM...');
        
        // Buscar cualquier texto que parezca nombre de persona en toda la página
        const allElements = document.querySelectorAll('*');
        const possibleCustomers = [];
        
        for (const element of allElements) {
            const text = element.textContent?.trim() || '';
            // Buscar texto que parezca nombre de persona
            if (text && 
                text.length > 3 && 
                text.length < 50 && 
                !text.includes('€') && 
                !text.includes('Payment') && 
                !text.includes('Cash') && 
                !text.includes('Bank') && 
                !text.includes('Validate') &&
                !text.includes('Back') &&
                !text.includes('Total') &&
                !text.includes('Change') &&
                !text.includes('Remaining') &&
                !text.includes('Walk-in') &&
                !text.includes('Customer') &&
                !text.includes('Account') &&
                !text.includes('Method') &&
                !text.includes('Due') &&
                !text.match(/^\d+$/) && // No solo números
                !text.match(/^[A-Z\s]+$/) && // No solo mayúsculas (botones)
                element.children.length === 0) { // Solo elementos hoja
                
                possibleCustomers.push({
                    text: text,
                    element: element,
                    classes: element.className,
                    id: element.id,
                    tagName: element.tagName
                });
            }
        }
        
        console.log('🔍 Posibles clientes encontrados:', possibleCustomers);
        
        // Si encontramos posibles clientes, usar el primero que parezca más relevante
        if (possibleCustomers.length > 0) {
            // Filtrar clientes más relevantes (excluir elementos técnicos)
            const relevantCustomers = possibleCustomers.filter(customer => 
                !customer.text.includes('body') &&
                !customer.text.includes('Orders') &&
                !customer.text.includes('Mitchell Admin') &&
                !customer.text.includes('Summary') &&
                !customer.text.includes('0.00') &&
                !customer.text.includes('Debug Window') &&
                !customer.text.includes('Electronic Scale') &&
                !customer.text.includes('Set Weight') &&
                !customer.text.includes('Reset') &&
                !customer.text.includes('Barcode Scanner') &&
                !customer.text.includes('Scan') &&
                customer.text.length > 2
            );
            
            console.log('🔍 Clientes relevantes filtrados:', relevantCustomers);
            
            if (relevantCustomers.length > 0) {
                const customer = relevantCustomers[0];
                console.log('📋 Usando cliente encontrado en debug:', customer.text);
                console.log('📋 Detalles del elemento:', {
                    tagName: customer.tagName,
                    classes: customer.classes,
                    id: customer.id
                });
                return {
                    name: customer.text,
                    email: '',
                    vat: '',
                    l10n_latam_identification_type_id: null,
                    type_regime_id: null,
                    type_liability_id: null,
                    municipality_id: null
                };
            }
        }
        
        console.log('⚠️ No se encontró ningún cliente en ninguna estrategia');
        return null;
    }
    
    // Función para obtener datos completos del cliente desde el backend
    async function getCustomerDataFromBackend(customerName) {
        console.log('🔍 Obteniendo datos completos del cliente desde backend:', customerName);
        
        try {
            // Hacer petición al backend para obtener datos del cliente
            const response = await fetch('/pos_invoice_validation/get_partner_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    partner_name: customerName
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('📋 Datos del cliente obtenidos desde backend:', data);
                return data;
            } else {
                console.log('⚠️ Error al obtener datos del cliente desde backend');
                // Devolver objeto básico con datos vacíos para forzar validación
                return {
                    name: customerName,
                    email: '',
                    vat: '',
                    l10n_latam_identification_type_id: null,
                    type_regime_id: null,
                    type_liability_id: null,
                    municipality_id: null
                };
            }
        } catch (error) {
            console.log('⚠️ Error en petición al backend:', error);
            // Devolver objeto básico con datos vacíos para forzar validación
            return {
                name: customerName,
                email: '',
                vat: '',
                l10n_latam_identification_type_id: null,
                type_regime_id: null,
                type_liability_id: null,
                municipality_id: null
            };
        }
    }
    
    // Interceptar todos los clics
    document.addEventListener('click', function(event) {
        console.log('🖱️ Clic detectado en:', event.target);
        
        // Verificar si estamos en pantalla de pago
        if (!isPaymentScreen()) {
            return; // No estamos en pantalla de pago, ignorar
        }
        
        console.log('💳 Estamos en pantalla de pago');
        
        // Verificar si es un clic de validación
        if (!isValidationClick(event.target)) {
            return; // No es un clic de validación, ignorar
        }
        
        console.log('🚨 CLIC DE VALIDACIÓN DETECTADO - Iniciando validación...');
        
        // Obtener el elemento clickeable para bloqueo
        const clickableElement = event.target.closest('button, div, span, a, [role="button"]');
        
        // Bloquear el evento inmediatamente para evitar que se procese
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
        
        // Obtener datos del cliente de forma síncrona
        const customer = getCustomerData();
        
        if (!customer) {
            console.log('⚠️ No hay cliente seleccionado en la orden');
            showErrorMessage('Debe seleccionar un cliente para continuar con el pago.');
            return;
        }
        
        console.log('🔍 Validando cliente antes del pago:', customer);
        
        const validation = validateRequiredFields(customer, config);
        
        if (!validation.valid) {
            console.log('❌ VALIDACIÓN FALLIDA - BLOQUEANDO PAGO:', validation.message);
            showErrorMessage(validation.message);
            return;
        }
        
        console.log('✅ Cliente validado correctamente - Procediendo con el pago');
        showSuccessMessage('Cliente validado correctamente. Procesando pago...');
        
        // Si la validación es exitosa, permitir el pago simulando el clic original
        setTimeout(() => {
            clickableElement.click();
        }, 100);
        
    }, true); // Usar capture para interceptar antes que otros handlers
    
    console.log('✅ Sistema de interceptación global configurado');
}

// Configurar interceptación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 DOM cargado, configurando interceptación...');
    setupValidationInterception();
});

// También configurar cuando la página esté completamente cargada
window.addEventListener('load', function() {
    console.log('🔧 Página cargada, configurando interceptación...');
    setupValidationInterception();
});