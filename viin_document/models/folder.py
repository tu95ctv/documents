# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DocumentFolder(models.Model):
    _name = 'viin_document.folder'
    _description = 'Documents Folder'
    _parent_name = 'parent_folder_id'
    _order = 'sequence'

    @api.constrains('parent_folder_id')
    def _check_parent_folder_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive folders.'))

    def name_get(self):
        name_array = []
        for record in self:
            if self.env.context.get('hierarchical', True) and record.parent_folder_id:
                name_array.append((record.id, '%s / %s' % (record.parent_folder_id.name, record.name)))
            else:
                name_array.append((record.id, record.name))
        return name_array

    company_id = fields.Many2one('res.company', 'Company')
    parent_folder_id = fields.Many2one('viin_document.folder', string='Parent Folder', ondelete='cascade')
    name = fields.Char(required=True, translate=True)
    description = fields.Html(string='Description', translate=True)
    document_ids = fields.One2many('viin_document.document', 'folder_id', string='Documents')
    sequence = fields.Integer('Sequence', default=20)
    cate_tag_ids = fields.One2many('viin_document.tag.cate', 'folder_id',string='Tag Categories')
    write_group_ids = fields.Many2many('res.groups', string='Write Groups')
    read_group_ids = fields.Many2many('res.groups', 'viin_document_folder_read_groups', string='Read Groups')
    owner_only = fields.Boolean(string='Own Documents Only')

    