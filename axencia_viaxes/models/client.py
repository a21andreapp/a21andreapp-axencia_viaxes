# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Client(models.Model):
    _name = 'agency.client'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Cliente da axencia"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    member_number = fields.Integer(required=True)
    date_of_birth = fields.Date('Data de nacemento')
    years = fields.Integer('Anos', compute='calculate_age')

    @api.depends('date_of_birth')
    def calculate_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age