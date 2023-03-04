# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools.translate import _

class AgencyPlace(models.Model):
    _name = 'agency.place'
    _description = 'Lugar de destino'
    _actividad = 'Título actividade'
    #_prezo = 'Prezo da actividade'

    name = fields.Char('Lugar', required=True)
    description = fields.Text('Descrición', required=True)
    actividad = fields.Text('Nome actividade', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.cr.execute("SELECT id FROM res_currency WHERE name = 'EUR';"), readonly=True)
    prezo = fields.Monetary(string='Prezo actividade: ', currency_field='currency_id', widget='monetary', options={'currency_symbol': '€', 'currency_position': 'before'})

    state = fields.Selection([
        ('started', 'Comezado'),
        ('finished', 'Rematado'),
        ('pending', 'Pendente'),
        ('cancelled', 'Cancelado')],
        'State', default="pending")
    
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('started', 'finished'),
                   ('pending', 'started'),
                   ('pending', 'cancelled'),
                   ('started', 'cancelled'),
                   ('cancelled', 'pending'),
                   ('cancelled', 'started')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for proxecto in self:
            if proxecto.is_allowed_transition(proxecto.state, new_state):
                proxecto.state = new_state
            else:
                message = _('Non se pode cambiar o estado de %s a %s') % (proxecto.state, new_state)
                raise UserError(message)

    def make_finished(self):
        self.change_state('finished')

    def make_started(self):
        self.change_state('started')

    def make_cancelled(self):
        self.change_state('cancelled')

    def make_pending(self):
        self.change_state('pending')
