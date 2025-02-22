# -*- coding: utf-8 -*-
{
    'name': "Custom Authentication",

    'sequence': 1,
    'author': "My Company",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/oauth2_provider_config_views.xml',
        'views/menus.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}


