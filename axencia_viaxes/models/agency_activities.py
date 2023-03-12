# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

class AgencyActivities(models.Model):
    _name = 'agency.activity'
    _description = 'Lugar de destino'
    _actividad = 'Título actividade'

    location = fields.Many2one('agency.locations', string='Destino', required=True)
    description = fields.Text('Descrición', required=True)
    actividad = fields.Char('Nome actividade', required=True)
    num_persoas = fields.Selection(string = 'Número mínimo de persoas' , selection = [('1', '1'),('2', '2'),('3', '3'),('4','4'),('5','5'),('6', '6'),('7', '7'),('8', '8'),('+9','+9')], default="1", required = True)
    name = fields.Char(compute='_compute_name', store=True)

    #borra unha actividade
    def delete_activity(self):
        self.ensure_one()
        self.unlink() 

    @api.depends('actividad')
    def _compute_name(self):
        for record in self:
            record.name = self.actividad