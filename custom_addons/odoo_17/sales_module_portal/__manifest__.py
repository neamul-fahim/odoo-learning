# -*- coding: utf-8 -*-
{
    'name': "sales_module_portal",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/quotation_portal_views_and_menus/all_sales_order_portal_tree_view.xml',
        'views/quotation_portal_views_and_menus/sale_order_portal_form_view.xml',
        'views/quotation_portal_views_and_menus/sale_order_create_update_form_view.xml',
        'views/quotation_portal_views_and_menus/portal_my_home_menu_quotation.xml',
        'views/users_portal_views_and_menus/users_portal_tree_view.xml',
        'views/users_portal_views_and_menus/user_portal_form_view.xml',
        'views/users_portal_views_and_menus/menu_users_portal_my_home.xml',
        'views/sales_report_dashboard/sales_report_dashboard_portal.xml',
        'views/sales_report_dashboard/sales_report_template.xml',
        'views/sales_report_dashboard/menu_sales_report_dashboard_portal.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sales_module_portal/static/src/**/*',
            # ('include', 'web._assets_helpers'),
            # 'web/static/src/scss/pre_variables.scss',
            # 'web/static/lib/bootstrap/scss/_variables.scss',
            # ('include', 'web._assets_bootstrap'),
            # ('include', 'web._assets_core'),
        ],
    },

    # 'application': True,
    # 'installable': True,

}
