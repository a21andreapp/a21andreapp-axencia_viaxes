# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Flight(models.Model):
    _name = 'agency.flight'
    _description = "Voos dispoñibles"

    departure_point = fields.Char(required=True, string='Lugar de salida')
    num_escalas = fields.Integer(required=True, string='Número de escalas')
    escalas = fields.Char(required=True, string='Lugares de escala:')
    flight_date = fields.Date('Data de ida')
    currency_id = fields.Many2one('res.currency', string='Currency')
    prezo = fields.Monetary(string='Prezo', currency_field='currency_id', widget='monetary', options={'currency_symbol': '€', 'currency_position': 'before'})