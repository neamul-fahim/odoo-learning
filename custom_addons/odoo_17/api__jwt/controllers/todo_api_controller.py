import json
from odoo import http
from odoo.http import request
from ..decorator import jwt_token_required


class ToDoAPI(http.Controller):

    @http.route('/todo', type='json', auth='none', methods=['GET'])
    @jwt_token_required
    def get_user_tasks(self):
        user = request.env.user
        tasks = request.env['todo.task'].sudo().search([('user_id', '=', user.id)])
        return [{'id': task.id, 'name': task.name, 'is_done': task.is_done} for task in tasks]

    @http.route('/todo', type='json', auth='none', methods=['POST'], csrf=False)
    @jwt_token_required
    def create_task(self):
        data = json.loads(request.httprequest.data)
        if 'name' not in data:
            return {'error': 'Missing task name'}, 400

        user = request.env.user
        task = request.env['todo.task'].sudo().create({
            'name': data['name'],
            'is_done': data.get('is_done', False),
            'user_id': user.id
        })
        return {'id': task.id, 'name': task.name, 'is_done': task.is_done}

    @http.route('/todo/<int:task_id>', type='json', auth='none', methods=['PUT'], csrf=False)
    @jwt_token_required
    def update_task(self, task_id):
        data = json.loads(request.httprequest.data)
        user = request.env.user
        task = request.env['todo.task'].sudo().search([('id', '=', task_id), ('user_id', '=', user.id)])

        if not task:
            return {'error': 'Task not found or you are not authorized to update this task'}, 404

        task.write({
            'name': data.get('name', task.name),
            'is_done': data.get('is_done', task.is_done),
        })
        return {'id': task.id, 'name': task.name, 'is_done': task.is_done}

    @http.route('/todo/<int:task_id>', type='json', auth='none', methods=['DELETE'], csrf=False)
    @jwt_token_required
    def delete_task(self, task_id):
        user = request.env.user
        task = request.env['todo.task'].sudo().search([('id', '=', task_id), ('user_id', '=', user.id)])

        if not task:
            return {'error': 'Task not found or you are not authorized to delete this task'}, 404

        task.unlink()
        return {'message': 'Task deleted'}