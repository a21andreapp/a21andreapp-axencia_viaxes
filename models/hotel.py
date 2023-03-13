# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

class Hotel(models.Model):
    _name = 'agency.hotel'
    _description = 'Hoteles que ofrece a axencia de viaxes'

    hotel_name = fields.Char(string='Nome do hotel', required=True)
    location = fields.Char(string='Ubicación', required=True)
    city = fields.Many2one('agency.locations', string='Cidade', required=True)
    prezo = fields.Float(string='Prezo/noite', digits=(4, 2), required=True, default = 0.0)
    name = fields.Char(compute='_compute_name', store=True)

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