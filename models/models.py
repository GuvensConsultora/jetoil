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

        """
        Al confirmar el wizard, inyectamos el contexto 'force_account_payment_create'.
        Esto le da permiso a todo lo que ocurra después (incluido el reject del cheque)
        para crear pagos sin necesidad de un Grupo de Pagos.
        """
        # 1. Preparamos el contexto VIP
        ctx = self._context.copy()
        ctx.update({'force_account_payment_create': True})
        
        # 2. Llamamos al método original pero CON el contexto VIP
        res = super(AccountCheckActionWizard, self.with_context(ctx)).action_confirm()
        
        return res
