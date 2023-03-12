# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import UserError
from odoo.tools.translate import _

class Client(models.Model):
    _name = 'agency.client'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Cliente da axencia"

    partner_id = fields.Many2one('res.partner', ondelete='cascade', string='Nome', readonly=False, required=True)
    date_of_birth = fields.Date('Data de nacemento', required=True)
    years = fields.Integer('Anos', compute='calculate_age', readonly=True)
    email = fields.Char(string='Correo electrónico', readonly=False)
    phone = fields.Char(string='Teléfono', required=True, readonly=False)
    dni = fields.Char(string='DNI', required=True, readonly=False)
    id = fields.Integer(string='ID cliente', readonly=True)
    compras = fields.One2many('agency.sales', 'client_name', string='Compras', readonly=True)
    
    # calcular a idade según a data de nacemento e controlar os posibles erros
    @api.depends('date_of_birth')
    def calculate_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                birth_date = record.date_of_birth
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.years = age
                if birth_date > today:
                    raise UserError(_('A data de nacemiento non pode ser futura.'))
                elif birth_date > today - timedelta(days=18*365):
                    raise UserError(_('Debe ser maior de 18 anos para crear unha conta.'))
            else:
                record.years = False

    # comprobar si é válida a dirección de email introducida
    @api.constrains('email')
    def validate_email(self):
        for record in self:
            if record.email:
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(pattern, record.email):
                    raise UserError(_('A dirección de correo electrónico introducida non é válida.'))

    # comproba se o número de teléfono introducido é válido
    @api.constrains('phone')
    def check_telefono(self):
        pattern = r"^\d{9}$"  # patrón para un número de teléfono de 9 díxitos
        if self.phone and not re.match(pattern, self.phone):
            raise UserError(_('O número de teléfono introducido non é válido.'))
        

    # comproba se o dni introducido é válido
    @api.constrains('dni')
    def _check_dni(self):
        for partner in self:
            if partner.dni:
                pattern = re.compile(r'^\d{8}[A-Z]$')
                if not pattern.match(partner.dni):
                    raise UserError(_('O DNI introducido non é válido'))

    # creamos un id único para cada cliente
    @api.model
    def create(self, vals):
        if vals.get('id', 'New') == 'New':
            vals['id'] = self.env['ir.sequence'].next_by_code('loan.sequence') or 'Error'
        return super(Client, self).create(vals)
