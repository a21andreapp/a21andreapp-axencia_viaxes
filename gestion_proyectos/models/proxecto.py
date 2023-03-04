# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools.translate import _

class Proxecto(models.Model):
    _name = 'mimodulo.proxecto'
    _description = 'Proxecto'

    name = fields.Char('Título Proxecto', required=True)
    description = fields.Text('Descrición', required=True)
    start_date = fields.Date('Data comezo')
    #autor_ids = fields.Many2many('res.partner', string='Participantes')
    #category_id = fields.Many2one('mimodulo.proxecto.category', string='Catergoría')

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

    def change_release_date(self):
        self.ensure_one()
        self.start_date = fields.Date.today()
    