# -*- coding: utf-8 -*-
{
    'name': "Documents Managers",  # Module title
    'summary': "Documents Managers",  # Module subtitle phrase
    'description': """
Documents Managers
==============
Documents Managers
    """,  # Supports reStructuredText(RST) format
    'author': "Dung",
    'version': '1.1',
    'depends': ['base','documents'],
    'data': [        
        'views/documents_manager.xml',        
        'views/menu.xml',
    ],
    'qweb': ["static/src/xml/documents_manager.xml"],
}