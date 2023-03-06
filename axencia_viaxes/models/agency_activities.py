# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools.translate import _

class AgencyActivities(models.Model):
    _name = 'agency.activity'
    _description = 'Lugar de destino'
    _actividad = 'Título actividade'

    name = fields.Char('Lugar', required=True)
    description = fields.Text('Descrición', required=True)
    actividad = fields.Text('Nome actividade', required=True)
    num_persoas = fields.Char('Número mínimo de persoas', required=True)
    #currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.cr.execute("SELECT id FROM res_currency WHERE name = 'EUR'"), readonly=True)
    #prezo = fields.Monetary(string='Prezo paquete: ', currency_field='currency_id', widget='monetary', options={'currency_symbol': '€', 'currency_position': 'before'})