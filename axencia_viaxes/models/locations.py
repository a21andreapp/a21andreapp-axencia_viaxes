# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api

logger = logging.getLogger(__name__)

class Locations(models.Model):
    _name = 'agency.locations'
    _description = 'Ventas de voos e actividades'

    id = fields.Integer(string='id', readonly=True)
    location = fields.Char(string='Destino', required=True)
    airport = fields.Char(string='Aeroporto', required=True)
    name = fields.Char(compute='_compute_name', store=True)

    @api.depends('location', 'airport')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.location} - {record.airport}"

    @api.model
    def create(self, vals):
        if vals.get('id', 'New') == 'New':
            vals['id'] = self.env['ir.sequence'].next_by_code('loan.sequence') or 'Error'
        return super(Locations, self).create(vals)