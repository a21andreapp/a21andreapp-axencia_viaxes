# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date
from odoo.exceptions import UserError

class Flight(models.Model):
    _name = 'agency.flight'
    _description = "Voos dispoñibles"

    departure_point = fields.Char(required=True, string='Lugar de salida')
    destination_point = fields.Char(required=True, string='Lugar de destino')
    num_escalas = fields.Integer(required=True, string='Número de escalas')
    escalas = fields.Char(string='Lugares de escala:', compute='escala')
    flight_hour = fields.Datetime('Hora de ida')
    flight_hour_arrival = fields.Datetime('Hora de chegada')
    currency_id = fields.Many2one('res.currency', string='Currency')
    prezo = fields.Monetary(string='Prezo', currency_field='currency_id', widget='monetary', options={'currency_symbol': '€', 'currency_position': 'before'})

    state = fields.Selection([
        ('draft', 'Dispoñible'),
        ('finished', 'Rematado'),
        ('cancelled', 'Cancelado'),
        ('agotado','Agotado')],
        'State', default="draft")
    
    def escala(self):
        for flight in self:
            if flight.num_escalas == 0:
                flight.escalas = "Sen escalas"
            elif flight.num_escalas > 0:
                flight.escalas = fields.Char()

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'cancelled'),
                   ('draft', 'finished'),
                   ('draft', 'agotado'),
                   ('cancelled', 'draft'),
                   ('agotado', 'draft'),
                   ('agotado','finished')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for flight in self:
            if flight.is_allowed_transition(flight.state, new_state):
                flight.state = new_state
            else:
                message = ('Moving from %s to %s is not allow') % (flight.state, new_state)
                raise UserError(message)

    def make_cancelled(self):
        self.change_state('cancelled')


    def make_finished(self):
        today = datetime.today()
        for flight in self:
            finish_date = flight.flight_hour_arrival
            if finish_date >= today:
                self.change_state('finished')
            else:
                message = ('Non se pode marcar como rematado porque a hora de chegada non coincide coa hora actual %s') % (today)
                raise UserError(message) 

    def make_agotado(self):
        self.change_state('agotado')

    def make_draft(self):
        self.change_state('draft')