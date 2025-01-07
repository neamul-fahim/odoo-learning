from odoo import models, fields


class ProjectTaskPortalUser(models.Model):
    _inherit = 'project.task'

    portal_user_ids = fields.Many2many(
        'res.users',  # Target model
        relation='project_task_portal_user_rel',  # Custom table name
        column1='task_id',  # Column for task ID
        column2='portal_user_id',  # Column for user ID
        string='Portal Assignees',  # Field label
        tracking=True,  # Enable tracking
        domain="[('share', '=', True), ('active', '=', True)]"  # Only portal users who are active
    )

