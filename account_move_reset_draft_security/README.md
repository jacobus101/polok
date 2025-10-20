# Account Move Reset to Draft Security

Restringe el botón **Restablecer a borrador** (`button_draft`) en `account.move` para todos los usuarios,
excepto quienes pertenezcan al grupo **Permitir Reset a Borrador (Facturas/Asientos)**.

## Instalación
1. Copia esta carpeta dentro de `addons/`.
2. Actualiza apps y instala el módulo **Account Move Reset to Draft Security**.
3. Asigna el grupo `account_move_reset_draft_security.group_account_move_reset_to_draft` a los usuarios autorizados.

## Seguridad en doble capa
- **UI:** el botón se oculta mediante atributo `groups` en la vista.
- **Backend:** se bloquea la llamada y se lanza `AccessError` si no se tiene el grupo.
