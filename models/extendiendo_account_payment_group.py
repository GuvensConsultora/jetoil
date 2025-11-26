# -*- coding: utf-8 -*-
from odoo import models, api

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.constrains('payment_group_id', 'payment_type')
    def check_payment_group(self):
        """
        Sobreescribimos la restricción de Odoo Argentina.
        Si traemos la llave 'force_account_payment_create' en el contexto,
        nos saltamos la validación y no hacemos nada (return).
        Si no la traemos, llamamos a super() para que ADHOC valide como siempre.
        """
        # 1. Chequeo del Pase VIP
        if self._context.get('force_account_payment_create'):
            print(">>> JETOIL: Saltando validación de Grupo de Pagos gracias al Pase VIP")
            return # Salimos de la función sin error. ¡Éxito!

        # 2. Si no hay pase, ejecutamos la validación original (la que pegaste tú)
        return super(AccountPayment, self).check_payment_group()
