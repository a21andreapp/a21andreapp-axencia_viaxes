# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

class Hotel(models.Model):
    _name = 'agency.hotel'
    _description = 'Hoteles que ofrece a axencia de viaxes'

    hotel_name = fields.Char(string='Nome do hotel', required=True)
    location = fields.Char(string='Ubicación', required=True)
    city = fields.Char(string='Cidade', required=True)
    prezo = fields.Float(string='Prezo/noite', digits=(4, 2), required=True, default = 0.0)
    name = fields.Char(compute='_compute_name', store=True)
    num_dias = fields.Integer(string='Número de días', required=True)
    prezo_total = fields.Float(string='Prezo total', digits=(4, 2), readonly=True, compute='calcular_prezo_total')

    @api.depends('prezo','num_dias')
    def calcular_prezo_total(self):
        for record in self:
            record.prezo_total = record.prezo * record.num_dias

    # comprobar que o número de días non sexa 0
    @api.depends('num_dias')
    def _check_num_dias(self):
        for record in self:
            if record.num_dias <= 0:
                raise UserError(_('O número de días debe ser maior a 0'))
            
    @api.constrains('num_dias')
    def _check_num_dias_constrains(self):
        self._check_num_dias()

    #borra un hotel
    def delete_activity(self):
        self.ensure_one()
        self.unlink() 

    @api.depends('hotel_name')
    def _compute_name(self):
        for record in self:
            record.name = self.hotel_name

    # calcular que o prezo por noite do hotel non sexa de 0€
    @api.depends('prezo')
    def _check_precio_not_zero(self):
        for record in self:
            if record.prezo <= 0:
                raise UserError(_('O prezo do hotel por noite non pode ser de 0€'))
            
    @api.constrains('prezo')
    def _check_precio_constrains(self):
        self._check_precio_not_zero()