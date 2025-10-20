# POS Electronic Invoice Validation

Módulo que valida y exige campos obligatorios para garantizar la facturación electrónica en el Point of Sale de Odoo 16.

## Características

- **Validación obligatoria de email** para facturación electrónica
- **Validación de NIT/Documento de identidad** (vat) para DIAN
- **Validación de tipo de identificación** (l10n_latam_identification_type_id)
- **Validación de régimen fiscal** (type_regime_id) para DIAN
- **Validación de responsabilidad fiscal** (type_liability_id) para DIAN
- **Validación de municipio** (municipality_id) para DIAN
- **Configuración flexible** por punto de venta
- **Bloqueo de selección** para clientes sin campos obligatorios
- **Mensajes de error estándar** de Odoo
- **Integración completa** con el POS
- **Compatible con l10n_co_edi_jorels** para facturación electrónica colombiana

## Dependencias

- `point_of_sale` - Módulo base del POS
- `l10n_co_edi_jorels` - Para campos fiscales colombianos

## Campos Validados

### 1. Email (email)
- **Obligatorio**: Sí
- **Validación**: Formato de email válido
- **Mensaje**: "El correo electrónico es obligatorio para clientes del POS"

### 2. NIT/Documento (vat)
- **Obligatorio**: Sí
- **Validación**: Entre 6 y 15 dígitos
- **Mensaje**: "El NIT/Documento de identidad es obligatorio para clientes del POS"

### 3. Tipo de Identificación (l10n_latam_identification_type_id)
- **Obligatorio**: Sí
- **Validación**: Debe estar seleccionado
- **Mensaje**: "El tipo de identificación es obligatorio para clientes del POS"

### 4. Régimen Fiscal (type_regime_id)
- **Obligatorio**: Sí
- **Dependencia**: l10n_co_edi_jorels
- **Validación**: Debe estar seleccionado
- **Mensaje**: "El régimen fiscal es obligatorio para clientes del POS"

### 5. Responsabilidad Fiscal (type_liability_id)
- **Obligatorio**: Sí
- **Dependencia**: l10n_co_edi_jorels
- **Validación**: Debe estar seleccionado
- **Mensaje**: "La responsabilidad fiscal es obligatoria para clientes del POS"

### 6. Municipio (municipality_id)
- **Obligatorio**: Sí
- **Dependencia**: l10n_co_edi_jorels
- **Validación**: Debe estar seleccionado
- **Mensaje**: "El municipio es obligatorio para clientes del POS"

## Instalación

1. Copiar el módulo a la carpeta `addons/`
2. Actualizar la lista de módulos
3. Instalar el módulo `POS Customer Validation`
4. Reiniciar el servicio de Odoo

## Uso

Una vez instalado, el módulo validará automáticamente todos los campos obligatorios:

- **Al seleccionar un cliente** en el POS
- **Al guardar un contacto** desde el POS
- **Al procesar un pago** con cliente asignado

Si algún campo obligatorio falta, se mostrará un mensaje de error y se bloqueará la acción.

## Configuración

### Configuración en el POS

1. **Ir a Configuración > Punto de Venta**
2. **Seleccionar la configuración del POS**
3. **En la pestaña "Configuración"**, buscar la sección **"Validación de Clientes"**
4. **Activar/Desactivar** los campos obligatorios para facturación electrónica:
   - ✅ **Requerir Email para Clientes** - Obligatorio para envío de facturas electrónicas
   - ✅ **Requerir NIT/Documento para Clientes** - Obligatorio para DIAN
   - ✅ **Requerir Tipo de Identificación para Clientes** - Obligatorio para DIAN
   - ✅ **Requerir Régimen Fiscal para Clientes** - Obligatorio para DIAN
   - ✅ **Requerir Responsabilidad Fiscal para Clientes** - Obligatorio para DIAN
   - ✅ **Requerir Municipio para Clientes** - Obligatorio para DIAN

### Configuración por Defecto

Por defecto, **todos los campos están habilitados** para garantizar el cumplimiento de la facturación electrónica. Puedes desactivar campos específicos según tu configuración de negocio.

### Dependencias

- **l10n_co_edi_jorels**: Requerido para campos fiscales colombianos (régimen, responsabilidad, municipio)
- **point_of_sale**: Módulo base del POS

## Soporte

Para reportar problemas o solicitar funcionalidades, crear un issue en el repositorio del proyecto.