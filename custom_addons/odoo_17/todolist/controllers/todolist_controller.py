# controllers/main.py
from odoo import http
from odoo.http import request
from werkzeug.security import generate_password_hash, check_password_hash


class TodoApp(http.Controller):

    @http.route('/todo/signup', type='http', auth='public', website=True, methods=['GET', 'POST'],csrf=False)
    def signup_todo(self, **kwargs):
        if request.httprequest.method == 'POST':
            email = kwargs.get('email')
            password = kwargs.get('password')

            # Check if the user already exists
            existing_user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
            if existing_user:
                return request.render('todolist.signup_template', {'error': 'User already exists'})

            # Create a new user
            user = request.env['res.users'].sudo().create({
                'name': email,
                'login': email,
                'password': password,
            })
            return request.redirect('/todo/login')

        if request.httprequest.method == 'GET':
            return request.render('todolist.signup_template')

    @http.route('/todo/login', type='http', auth='public', website=True, methods=['GET', 'POST'],csrf=False)
    def login_todo(self, **kwargs):
        if request.httprequest.method == 'POST':
            email = kwargs.get('email')
            password = kwargs.get('password')

            # Authenticate the user using Odoo's session-based system
            user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
            if not user:
                return request.render('todolist.login_template', {'error': 'Invalid email or password'})

            # Attempt to log in the user using Odoo's session-based authentication
            try:
                request.session.authenticate(request.env.cr.dbname, email, password)
                return request.redirect('/my_todo')
            except Exception as e:
                return request.render('todolist.login_template', {'error': 'Invalid email or password'})

        if request.httprequest.method == 'GET':
            return request.render('todolist.login_template')

    @http.route('/todo/logout', type='http', auth='user', website=True,csrf=False)
    def logout(self, **kwargs):
        request.session.logout()
        return request.redirect('/todo/login')

    @http.route('/my_todo', type='http', auth='user', website=True,csrf=False)
    def todo_list(self, **kwargs):
        tasks = request.env['todolist'].sudo().search([('user_id', '=', request.env.user.id)])
        return request.render('todolist.todo_grid', {'tasks': tasks})

    @http.route('/todo/task/<int:task_id>', type='http', auth='user', website=True,csrf=False)
    def todo_form(self, task_id, **kwargs):
        task = request.env['todolist'].sudo().browse(task_id)
        return request.render('todolist.task_form', {'task': task})

    @http.route('/todo/task/save', type='http', auth='user', website=True, methods=['POST','GET'],csrf=False)
    def save_task(self, **kwargs):
        if request.httprequest.method == 'POST':
            task_id = int(kwargs.get('task_id', 0))
            if task_id:
                task = request.env['todolist'].sudo().browse(task_id)
                task.write({
                    'name': kwargs.get('name', task.name),
                    'description': kwargs.get('description', task.description),
                    'is_done': kwargs.get('is_done') == 'on',
                })
            else:
                request.env['todolist'].sudo().create({
                    'name': kwargs.get('name'),
                    'description': kwargs.get('description'),
                    'user_id': request.env.user.id,
                    'is_done': kwargs.get('is_done') == 'on',
                })
            return request.redirect('/my_todo')

        if request.httprequest.method == 'GET':
            return request.render('todolist.task_form')

    @http.route('/todo/task/delete/<int:task_id>', type='http', auth='user', website=True,csrf=False)
    def delete_task(self, task_id, **kwargs):
        task = request.env['todolist'].sudo().browse(task_id)
        task.unlink()
        return request.redirect('/my_todo')
