from odoo import models, fields, _

class TotoList(models.Model):
    _name = 'todo.list'
    _description = 'Todo List'

    name = fields.Char(string='Task Name')
    completed = fields.Boolean(string='Completed')
    color = fields.Char(string='Color')
