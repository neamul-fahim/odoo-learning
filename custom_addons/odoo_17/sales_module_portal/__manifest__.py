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
        'views/portal_my_home_menu_quotation.xml',
        'views/all_sales_order_portal_tree_view.xml',
        'views/sale_order_portal_form_view.xml',
        'views/sale_order_create_update_form_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'sales_module_portal/static/src/js/sale_order_create_update_form_view.js',
    #     ],
    # },

    # 'application': True,
    # 'installable': True,

}
