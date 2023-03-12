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
   
   # comprobar que o cliente non teña compras sen pagar
    @api.model
    def create(self, vals):
        client_id = vals.get('client_name')
        if client_id:
            unpaid_sales = self.search([('client_name', '=', client_id), ('pagado', '=', False)])
            if unpaid_sales:
                raise UserError('O cliente xa ten unha compra sen pagar!!')
        return super(AgencySales, self).create(vals)
    
    @api.constrains('activities', 'flight_name.destination_point.location')
    def _check_activities_location(self):
        for record in self:
            if record.activities:
                for activity in record.activities:
                    if activity.location.location != self.flight_name.destination_point.location:
                        raise UserError('A localización da actividade non coincide coa localización de chegada do voo')

    @api.depends('client_name', 'flight_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{self.client_name.partner_id.name} ( {self.flight_name.departure_point.location} - {self.flight_name.destination_point.location})"

    # comprobar dispoñibilidade de un voo
    @api.model
    def comprobar_disponibilidad(self):
        if self.flight_name.state == 'agotado':
            raise UserError('Non se pode comprar un voo agotado')
        elif self.flight_name.state == 'cancelled':
            raise UserError('Non se pode comprar un voo cancelado')   
        elif self.flight_name.state == 'finished':
            raise UserError('Non se pode comprar un voo acabado')            

    @api.constrains('flight_name')    
    def action_confirm_reservation(self):
        self.comprobar_disponibilidad()