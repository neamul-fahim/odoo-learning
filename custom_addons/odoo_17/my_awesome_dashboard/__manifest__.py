# -*- coding: utf-8 -*-
{
    'name': "My Awesome Dashboard",

    'summary': """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,

    'description': """
        Starting module for "Discover the JS framework, chapter 2: Build a dashboard"
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials/AwesomeDashboard',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web', 'mail', 'crm'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'my_awesome_dashboard/static/src/dashboard/**/*',
            'my_awesome_dashboard/static/src/global_or_shared_state/**/*',
            'my_awesome_dashboard/static/src/todo_list/*.js',
            'my_awesome_dashboard/static/src/todo_list/*.xml',
            # 'my_awesome_dashboard/static/src/todo_list/*.scss',
        ],

    },
    'license': 'AGPL-3'
}
