# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Client(models.Model):
    _name = 'agency.client'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Cliente da axencia"

    partner_id = fields.Many2one('res.partner', ondelete='cascade', string='Nome')
    member_number = fields.Integer(required=True, string='Número de cliente')
    date_of_birth = fields.Date('Data de nacemento')
    years = fields.Integer('Anos', compute='calculate_age')

    @api.depends('date_of_birth')
    def calculate_age(self):
        for record in self:
            try:
                today = date.today()
                birth_date = record.date_of_birth
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.years = age
            except:
                record.years = 0
