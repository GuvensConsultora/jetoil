# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountCheckActionWizard(models.TransientModel):
    # Aquí le decimos a Odoo: "Quiero modificar este modelo existente"
    _inherit = 'account.check.action.wizard'

    def action_confirm(self):
        """
        Este método se ejecuta cuando pulsas el botón 'Confirm'.
        """
        # --- ZONA 1: ANTES DE LA ACCIÓN ORIGINAL ---
        # Aquí puedes poner validaciones o lógica previa.
        # Por ejemplo, imprimir en el log para ver que funciona:
        print("---------------------------------------------------------")
        print(">>> ¡HOLA! El módulo JETOIL ha interceptado el botón <<<")
        print(f"Fecha seleccionada: {self.date}")
        print("---------------------------------------------------------")

        print(">>> JETOIL WIZARD: Iniciando REPARACIÓN y confirmación...")

        # Obtenemos los cheques seleccionados
        active_ids = self._context.get('active_ids', [])
        checks = self.env['account.check'].browse(active_ids)

        for check in checks:
            # Buscamos las operaciones que causan el crash (sin origen)
            operaciones_rotas = check.operation_ids.filtered(lambda op: not op.origin)
            
            if operaciones_rotas:
                print(f">>> JETOIL: Reparando {len(operaciones_rotas)} operaciones rotas en cheque {check.id}")
                # EN LUGAR DE BORRAR, LAS REPARAMOS.
                # Les asignamos como origen el propio cheque.
                # Esto evita el error 'NoneType' y es inofensivo para la lógica.
                for op in operaciones_rotas:
                    op.write({'origin': 'account.check,%s' % check.id})
        """
        Al confirmar el wizard, inyectamos el contexto 'force_account_payment_create'.
        Esto le da permiso a todo lo que ocurra después (incluido el reject del cheque)
        para crear pagos sin necesidad de un Grupo de Pagos.
        """
        # 2. Preparamos el contexto VIP
        ctx = self._context.copy()
        ctx.update({'force_account_payment_create': True})
        
        # 2. Llamamos al método original pero CON el contexto VIP
        res = super(AccountCheckActionWizard, self.with_context(ctx)).action_confirm()
        
        return res
