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
    prezo = fields.Float(string='Prezo', digits=(4, 2), default = 0.0, readonly=True, compute='calcular_prezo_total')
    prezo_total_actividades = fields.Float(string='Prezo total actividades', digits=(4, 2), readonly=True, compute='calcular_prezo_total_actividades')
    num_dias = fields.Integer(string='Número de días', required=True)
    prezo_hotel = fields.Float(string='Prezo hotel', digits=(4, 2), readonly=True, compute='calcular_prezo_hotel')

    # comprobar que o número de días non sexa 0
    @api.depends('num_dias')
    def _check_num_dias(self):
        for record in self:
            if record.num_dias <= 0:
                raise UserError(_('O número de días debe ser maior a 0'))
      
    @api.constrains('num_dias')
    def _check_num_dias_constrains(self):
        self._check_num_dias()

    # calcular o prezo do hotel dependendo do días escollidos
    @api.depends('num_dias', 'hotel.prezo')
    def calcular_prezo_hotel(self):
        for record in self:
            total = record.hotel.prezo * record.num_dias
            record.prezo_hotel = total

    # calcular o prezo total das actividades seleccionadas
    @api.depends('activities')
    def calcular_prezo_total_actividades(self):
        for record in self:
            total = 0.0
            for activity in record.activities:
                total += activity.prezo
            record.prezo_total_actividades = total

    # calcular prezo total da venta
    @api.depends('prezo_total_actividades', 'prezo_hotel', 'flight_name.prezo')
    def calcular_prezo_total(self):     
        for record in self:
            total = record.prezo_total_actividades + record.flight_name.prezo + record.prezo_hotel
            record.prezo = total

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
    
    # comprobar que o destino da actividade e o destino do voo sexa o mesmo
    @api.constrains('activities', 'flight_name.destination_point.location')
    def _check_activities_location(self):
        for record in self:
            if record.activities:
                for activity in record.activities:
                    if activity.location.location != self.flight_name.destination_point.location:
                        raise UserError('A localización da actividade non coincide coa localización de chegada do voo')
                    
    # comprobar que o destino do hotel e o destino do voo sexa o mesmo
    @api.constrains('flight_name', 'hotel')
    def _check_hotel_location(self):
        if self.flight_name.destination_point.location != self.hotel.city.location:
            raise UserError('A localización do hotel non coincide coa localización de chegada do voo')

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