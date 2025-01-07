
from odoo import models, fields, api

class TodoTask(models.Model):
    _name = 'todolist'
    _description = 'Todo Task'

    name = fields.Char('Task Name', required=True)
    description = fields.Text('Description')
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    is_done = fields.Boolean('Done', default=False)
