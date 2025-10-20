# Account Move Reset to Draft Security

Permiso controlado por **casilla en Usuarios**:
- Campo en `res.users`: `can_reset_account_move`.
- Vista de `account.move`: oculta el botón si el usuario no tiene la casilla.
- **Backend**: sobrescribe `button_draft` y bloquea con `AccessError`.

## Instalación
1. Copiar en `addons/`.
2. Actualizar Apps e instalar.
3. En **Ajustes → Usuarios**, marca **Puede restablecer facturas a borrador** a quien corresponda.

## Notas
- La ocultación en UI usa un campo calculado `can_user_reset_to_draft` en `account.move` para que los `attrs` funcionen sin depender de grupos.
- La seguridad real se garantiza en backend.

## Pruebas
Incluye una prueba ligera que valida la existencia de los campos y la vista heredada.
