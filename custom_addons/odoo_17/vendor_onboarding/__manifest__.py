# -*- coding: utf-8 -*-
{
    'name': "vendor_onboarding",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/otp_page.xml',
        'views/signup_page.xml',
        'views/welcome_page.xml',
        'views/vendor_details_form.xml',
        'views/vendor_details_portal_form.xml',
        'views/all_vendor_accounts_portal_tree_view.xml',
        'views/vendor_onboarding_view.xml',
        'views/set_password_page.xml',
        'views/vendor_dashboard.xml',
        'views/portal.xml',
        'views/portal_my_home_menu_all_vendor_accounts.xml',
        'views/portal_my_home_menu_vendor_account.xml',
        'views/portal_my_home_menu_vendor_dashboard.xml',
        'views/views.xml',
        'views/menu.xml',
        'views/template_to_render_vendor_dashboard_component.xml',
        'views/all_vendor_accounts_portal_tree_view.xml',
        'views/project_task_form_view_inherit.xml',
        'views/custom_login_page.xml',
        'views/test.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'vendor_onboarding/static/src/vendor_dashboard/**/*',
    #     ],
    # },
    # 'assets': {
    #     'web.assets_backend': [
    #         'vendor_onboarding/static/src/vendor_dashboard/**/*',
    #     ],
    # },
    'assets': {
        'web.assets_frontend': [
            'vendor_onboarding/static/src/vendor_dashboard/**/*',
            # ('remove', 'vendor_onboarding/static/src/vendor_dashboard/test.js')

        ],
        'vendor_onboarding.my_vendor_assets': [
            ('include', 'web._assets_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap'),
            ('include', 'web._assets_core'),
            'vendor_onboarding/static/src/vendor_dashboard/**/*',
            # 'vendor_onboarding/static/src/vendor_dashboard/test.js',

        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
