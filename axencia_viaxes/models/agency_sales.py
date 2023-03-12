# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import datetime

logger = logging.getLogger(__name__)

class AgencySales(models.Model):
    _name = 'agency.sales'
    _description = 'Ventas de voos e actividades'

    id = fields.Integer(string='id', readonly=True)
    client_name = fields.Many2one('agency.client', string='Cliente', required=True)
    flight_name = fields.Many2one('agency.flight', string='Vuelo', required=True)
    hotel = fields.Many2one('agency.hotel', string='Hotel', required=True)
    activities = fields.Many2many('agency.activity', string='Lista de actividades', required=True)
    data_compra = fields.Date('Data compra', readonly=True, compute='set_date')
    pagado = fields.Boolean('Pagado', default=False)
    name = fields.Char(compute='_compute_name', store=True)

    def set_date(self):
        for sales in self:
            sales.data_compra = datetime.now()

    @api.depends('client_name', 'flight_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{self.client_name.partner_id.name} ( {self.flight_name.departure_point.location} - {self.flight_name.destination_point.location})"