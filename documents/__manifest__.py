# -*- coding: utf-8 -*-
{
    'name': "ViinDoo Documents",

    'summary': "ViinDoo Document management",

    'description': """
        App to upload and manage your documents.
    """,

    'author': "ViinDoo",
    'category': 'Productivity/Documents',
    'sequence': 80,
    'version': '1.0',
    'application': True,
    'website': '',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'portal', 'web', 'attachment_indexation', 'digest'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'data/digest_data.xml',
        # 'data/documents_data.xml',
        # 'data/workflow_data.xml',
        # 'data/files_data.xml',
        # 'data/mail_templates.xml',
        # 'views/assets.xml',

        'views/documents_views.xml',
        'views/documents_configs/documents_folder_views.xml',
        'views/documents_configs/res_config_settings_views.xml',
        'views/documents_configs/documents_share_views.xml',
        'views/documents_configs/documents_workflow_rule_views.xml',
        'views/documents_configs/documents_facet_views.xml',
        'views/documents_configs/documents_tag_views.xml',

        # 'views/documents_configs/res_partner.xml',

        # 'views/templates.xml',
        # 'views/activity_views.xml',
        # 'wizard/request_activity_views.xml',

        'views/menu.xml',
    ],

    'qweb': [
        # "static/src/xml/*.xml",
        # "static/src/owl/components/pdf_manager/pdf_manager.xml",
        # "static/src/owl/components/pdf_page/pdf_page.xml",
        # "static/src/owl/components/pdf_group_name/pdf_group_name.xml",
    ],

    'demo': [
        # 'demo/demo.xml',
    ],
    'license': 'OEEL-1',
}
