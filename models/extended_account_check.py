# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountCheck(models.Model):
    _inherit = 'account.check'

    def get_payment_values(self, journal):
        """
        Sobreescribimos este método de odoo-argentina para corregir el error
        de Singleton cuando el diario tiene múltiples métodos de pago.
        """
        # Obtenemos los métodos de pago permitidos por el diario
        payment_methods = journal._default_outbound_payment_methods()
        
        #raise UserError(f"Metodos de pago {payment_methods[1].name}")
        
        # --- CORRECCIÓN JETOIL ---
        # Si hay más de uno, nos quedamos solo con el primero (index 0)
        # para evitar el error 'Expected Singleton'
        if len(payment_methods) > 1:
            payment_method_id = payment_methods[1].id
        else:
            payment_method_id = payment_methods.id
        # -------------------------

        return {
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_type': 'supplier' if self.type == 'third_party' else 'customer',
            'journal_id': journal.id,
            'payment_type': 'outbound',
            'payment_date': fields.Date.context_today(self),
            'payment_method_id': payment_method_id, # Usamos nuestra variable corregida
            'check_ids': [(4, self.id, False)],
            'communication': 'Rechazo cheque %s' % self.number,
        }

    
