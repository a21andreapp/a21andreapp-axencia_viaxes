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
    prezo = fields.Float(string='Prezo', digits=(4, 2), required=True, default = 0.0)
    name = fields.Char(compute='_compute_name', store=True)

    #borra un hotel
    def delete_activity(self):
        self.ensure_one()
        self.unlink() 

    @api.depends('hotel_name')
    def _compute_name(self):
        for record in self:
            record.name = self.hotel_name