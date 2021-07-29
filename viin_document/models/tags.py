# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.osv import expression


class TagsCategories(models.Model):
    _name = "viin_document.tag.cate"
    _description = "Category"
    _order = "sequence, name"
    _sql_constraints = [
        ('name_unique', 'unique (folder_id, name)', "cate_tag already exists in this folder"),
    ]

    folder_id = fields.Many2one('viin_document.folder', string="Folder", ondelete="cascade")
    name = fields.Char(required=True, translate=True)
    tag_ids = fields.One2many('viin_document.tag', 'cate_tag_id')
    sequence = fields.Integer('Sequence', default=10)
    
class Tags(models.Model):
    _name = "viin_document.tag"
    _description = "Tag"
    _order = "sequence, name"
    _sql_constraints = [
        ('cate_tag_name_unique', 'unique (cate_tag_id, name)', "Tag already exists for this cate_tag"),
    ]

    folder_id = fields.Many2one('viin_document.folder', string="Folder", related='cate_tag_id.folder_id', store=True, readonly=False)
    cate_tag_id = fields.Many2one('viin_document.tag.cate', string="Category", ondelete='cascade', required=True)
    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)

    def name_get(self):
        names = []
        if self._context.get('simple_name'):
            return super(Tags, self).name_get()
        for record in self:
            names.append((record.id, "%s > %s" % (record.cate_tag_id.name, record.name)))
        return names

