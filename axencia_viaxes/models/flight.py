# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError
from odoo.tools.translate import _

class Flight(models.Model):
    _name = 'agency.flight'
    _description = "Voos dispoñibles"

    departure_point = fields.Char(required=True, string='Lugar de salida')
    destination_point = fields.Char(required=True, string='Lugar de destino')
    num_escalas = fields.Selection(required=True, string='Número de escalas', selection=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], default="0")
    escalas = fields.Char(string='Lugares de escala:', required=True)
    flight_hour = fields.Datetime('Hora de ida')
    flight_hour_arrival = fields.Datetime('Hora de chegada')
    prezo = fields.Float(string='Prezo', digits=(4, 2), required=True, default = 0.0)

    state = fields.Selection([
        ('draft', 'Dispoñible'),
        ('finished', 'Rematado'),
        ('cancelled', 'Cancelado'),
        ('agotado','Agotado')],
        'State', default="draft")

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
        if self.flight_hour_arrival >= today:
            self.change_state('finished')
        else:
            message = ('Non se pode marcar como rematado porque a hora de chegada non coincide coa hora actual %s') % (today)
            raise UserError(message)

    def make_agotado(self):
        self.change_state('agotado')

    def make_draft(self):
        self.change_state('draft')

    @api.onchange('num_escalas')
    def escala(self):
        if self.num_escalas == '0':
            # Poñer directamente sin escalas
            self.escalas = "Sen escalas"
        else:
            self.escalas = ""

    #borrar o rexistro de un voo
    def delete_flight(self):
        self.ensure_one()
        self.unlink()   

    # calcular que o prezo de un voo non sea de 0€
    @api.depends('prezo')
    def _check_precio_not_zero(self):
        for record in self:
            if record.prezo == 0:
                raise UserError(_('O prezo do voo non pode ser de 0€'))
    
    @api.constrains('prezo')
    def _check_precio_constrains(self):
        self._check_precio_not_zero()