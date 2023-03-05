# -*- coding: utf-8 -*-
{
    'name': "Axencia de viaxes",
    'summary': "Obtén información e regala a mellor das túas viaxes",
    'description': "Long description of module's purpose",

    'author': "Andrea Peteiro Piñeiro",
    'website': "http://www.yourcompany.com",
    'category': 'Tools',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/tour_packages.xml',
        'views/client.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}