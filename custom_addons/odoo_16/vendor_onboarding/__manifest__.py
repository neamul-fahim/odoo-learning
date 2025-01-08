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
    'depends': ['base'],

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
        'views/views.xml',
        'views/menu.xml',
        'views/vendor_dashboard_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'vendor_onboarding/static/src/**/*',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
