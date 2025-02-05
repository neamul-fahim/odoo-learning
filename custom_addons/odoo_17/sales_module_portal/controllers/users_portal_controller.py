from odoo.addons.portal.controllers.portal import CustomerPortal,pager
from odoo import http
from odoo.http import request

class UsersPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'user_count_portal' in counters:

            values['user_count_portal'] = 1
        return values


    @http.route(['/my/users', '/users/page/<int:page>'], type='http', auth='user', methods=['GET'], website=True)
    def all_users(self, page=1, sortby='id', **kw):
        # Define sort options

        print(f'==================================users page====================')
        sort_query_list = {
            'id': {'label': 'ID', 'order': 'id desc'},
            'name': {'label': 'Name', 'order': 'name asc'},
            'email': {'label': 'Email', 'order': 'email asc'},
        }
        default_order_by = sort_query_list[sortby]['order']

        # Check if the user has admin permissions
        user = request.env.user
        is_admin = user.has_group('sales_team.group_sale_manager')  # Adjust the group ID if needed
        is_admin_portal = user.has_group('sales_module_portal.group_sale_manager_portal')

        if is_admin or is_admin_portal:
            domain = []
        else:
            domain = [('id', '=', False)]  # No records will match this


        # Get total count and fetch paginated records
        total_users = request.env['res.users'].sudo().search_count(domain)
        page_details = pager(
            url='/users',
            total=total_users,
            page=page,
            step=3,
            url_args={'3': sortby},
        )
        all_users = request.env['res.users'].sudo().search(
            domain, limit=3, order=default_order_by, offset=page_details['offset']
        )

        # Now, let's fetch relevant info for each user for the tree view
        users_info = []
        for user in all_users:
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                # 'team': user.team_id.name if user.team_id else 'N/A',
                # 'sales_orders_count': len(user.sale_order_ids),  # Sales orders count
                # 'role': ', '.join(user.groups_id.mapped('name')),  # User's roles/groups
            }
            users_info.append(user_data)

        # Prepare data for rendering in tree view
        vals = {
            'users': users_info,  # Enriched data for the tree view
            'page_name': 'users',
            'pager': page_details,
            'sortby': sortby,
            'searchbar_sortings': sort_query_list,
        }
        return request.render('sales_module_portal.users_portal_tree_view', vals)

    @http.route('/user/<int:user_id>', type='http', auth='public', methods=['GET'], website=True)
    def user(self, user_id, **kw):
        user_record = http.request.env['res.users'].sudo().browse(user_id)

        # Check if the user exists
        if not user_record.exists():
            return http.request.not_found()

        # Get the groups the user belongs to
        # user_groups = user_record.groups_id
        # Fetch all groups
        sales_groups = [
            {
                'name': 'salesman',
                'value': user_record.has_group('sales_module_portal.group_sale_salesman_portal'),
                'id': request.env.ref('sales_module_portal.group_sale_salesman_portal').id
            },
            {
                'name': 'all_leads',
                'value': user_record.has_group('sales_module_portal.group_sale_salesman_all_leads_portal'),
                'id': request.env.ref('sales_module_portal.group_sale_salesman_all_leads_portal').id
            },
            {
                'name': 'sale_manager',
                'value': user_record.has_group('sales_module_portal.group_sale_manager_portal'),
                'id': request.env.ref('sales_module_portal.group_sale_manager_portal').id
            }
        ]

        vals = {
            'doc': user_record,
            'page_name': 'user',
            'sales_groups': sales_groups,
            # 'user_groups': user_groups,  # Pass groups to the template
        }

        # Get the list of all users and determine the previous and next records
        user_records = http.request.env['res.users'].search([])
        user_records_ids = user_records.mapped('id')
        user_record_index = user_records_ids.index(user_id)

        if user_record_index > 0:
            vals['prev_record'] = f'/user/{user_records_ids[user_record_index - 1]}'
        if user_record_index < len(user_records_ids) - 1:
            vals['next_record'] = f'/user/{user_records_ids[user_record_index + 1]}'

        return http.request.render('sales_module_portal.user_portal_form_view', vals)

    @http.route('/user/group/assign', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def assign_group(self, **kwargs):
        user_id = int(kwargs.get('user_id'))
        group_id = int(kwargs.get('group_id'))
        action = kwargs.get('action')

        user = request.env['res.users'].sudo().browse(user_id)
        group = request.env['res.groups'].sudo().browse(group_id)

        if user.exists() and group.exists():
            if action == 'add':
                group.sudo().write({'users': [(4, user.id)]})
            elif action == 'remove':
                group.sudo().write({'users': [(3, user.id)]})

        return request.redirect(f'/user/{user_id}')







    # @http.route('/user/add_group', type='json', auth='user', methods=['POST'])
    # def add_to_group(self, user_id, group_id):
    #     user = request.env['res.users'].sudo().browse(user_id)
    #     group = request.env['res.groups'].sudo().browse(group_id)
    #
    #     if user.exists() and group.exists():
    #         user.write({'groups_id': [(4, group.id)]})
    #         return {'status': 'success', 'message': 'User added to group successfully'}
    #     return {'status': 'error', 'message': 'User or group not found'}
    #
    # @http.route('/user/remove_group', type='json', auth='user', methods=['POST'])
    # def remove_from_group(self, user_id, group_id):
    #     user = request.env['res.users'].sudo().browse(user_id)
    #     group = request.env['res.groups'].sudo().browse(group_id)
    #
    #     if user.exists() and group.exists():
    #         user.write({'groups_id': [(3, group.id)]})  # Remove the group from the user
    #         return {'status': 'success', 'message': 'User removed from group successfully'}
    #     return {'status': 'error', 'message': 'User or group not found'}