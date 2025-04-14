# Restrict Quick Create in Bank Statements

Este módulo restringe la funcionalidad de creación rápida en los extractos bancarios para usuarios que no tienen permisos de contabilidad en Odoo 12.

## Características

- Deshabilita la creación rápida de ubicaciones en el formulario de extractos bancarios
- Deshabilita la creación rápida de tipos de operación
- Evita la creación de líneas mediante el botón "Agregar línea" para usuarios sin permisos de contabilidad
- Utiliza los grupos de seguridad estándar de contabilidad de Odoo

## Requisitos

- Odoo 12.0
- Módulo de Contabilidad (account)

## Instalación

1. Copiar el módulo en la carpeta de addons de Odoo
2. Actualizar la lista de módulos
3. Instalar el módulo "Restrict Quick Create in Bank Statements"

## Configuración

No se requiere configuración adicional. El módulo utiliza los grupos de seguridad existentes de contabilidad.

## Uso

Los usuarios que no pertenezcan al grupo "Contabilidad" no podrán:
- Crear nuevas ubicaciones desde el formulario de extractos bancarios
- Crear nuevos tipos de operación
- Agregar líneas mediante el botón de creación rápida

## Soporte

Para soporte y consultas, contactar a:
- Email: soporte@polok.com 