from odoo import models, fields, api



class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'ToDo Task'

    name = fields.Char(string='Task', required=True)
    is_done = fields.Boolean(string='Done')
    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(comodel_name='res.users', string='User')
