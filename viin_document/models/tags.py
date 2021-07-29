# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.osv import expression


class TagsCategories(models.Model):
    _name = "viin_document.tag.cate"
    _description = "Category"
    _order = "sequence, name"

    # the colors to be used to represent the display order of the cate_tags (tag categories), the colors
    # depend on the order and amount of fetched categories
    # currently used in the searchPanel and the kanban view and should match across the two.
    #mở lại để test
    cate_tag_ORDER_COLORS = ['#F06050', '#6CC1ED', '#F7CD1F', '#814968', '#30C381', '#D6145F', '#475577', '#F4A460',
                          '#EB7E7F', '#2C8397']

    folder_id = fields.Many2one('viin_document.folder', string="Folder", ondelete="cascade")
    name = fields.Char(required=True, translate=True)
    tag_ids = fields.One2many('viin_document.tag', 'cate_tag_id')
    sequence = fields.Integer('Sequence', default=10)
    tooltip = fields.Char(help="Text shown when hovering on this tag category or its tags", string="Tooltip")

    _sql_constraints = [
        ('name_unique', 'unique (folder_id, name)', "cate_tag already exists in this folder"),
    ]


class Tags(models.Model):
    _name = "viin_document.tag"
    _description = "Tag"
    _order = "sequence, name"

    folder_id = fields.Many2one('viin_document.folder', string="Folder", related='cate_tag_id.folder_id', store=True,
                                readonly=False)
    cate_tag_id = fields.Many2one('viin_document.tag.cate', string="Category", ondelete='cascade', required=True)
    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer('Sequence', default=10)

    _sql_constraints = [
        ('cate_tag_name_unique', 'unique (cate_tag_id, name)', "Tag already exists for this cate_tag"),
    ]

    def name_get(self):
        names = []
        if self._context.get('simple_name'):
            return super(Tags, self).name_get()
        for record in self:
            names.append((record.id, "%s > %s" % (record.cate_tag_id.name, record.name)))
        return names

    @api.model
    def _get_tags(self, domain, folder_id):
        """
        fetches the tag and cate_tag ids for the document selector (custom left sidebar of the kanban view)
        """
        documents = self.env['viin_document.document'].search(domain)
        # folders are searched with sudo() so we fetch the tags and cate_tags from all the folder hierarchy (as tags
        # and cate_tags are inherited from ancestor folders).
        folders = self.env['viin_document.folder'].sudo().search([('parent_folder_id', 'parent_of', folder_id)])
        self.flush(['sequence', 'name', 'cate_tag_id'])
        self.env['viin_document.tag.cate'].flush(['sequence', 'name', 'tooltip'])
        query = """
            SELECT  tag_cate.sequence AS group_sequence,
                    tag_cate.id AS group_id,
                    tag_cate.tooltip AS group_tooltip,
                    viin_document_tag.sequence AS sequence,
                    viin_document_tag.id AS id,
                    COUNT(rel.viin_document_document_id) AS __count
            FROM viin_document_tag
                JOIN viin_document_tag_cate tag_cate ON viin_document_tag.cate_tag_id = tag_cate.id
                    AND tag_cate.folder_id = ANY(%s)
                LEFT JOIN document_tag_rel rel ON viin_document_tag.id = rel.viin_document_tag_id
                    AND rel.viin_document_document_id = ANY(%s)
            GROUP BY tag_cate.sequence, tag_cate.name, tag_cate.id, tag_cate.tooltip, viin_document_tag.sequence, viin_document_tag.name, viin_document_tag.id
            ORDER BY tag_cate.sequence, tag_cate.name, tag_cate.id, tag_cate.tooltip, viin_document_tag.sequence, viin_document_tag.name, viin_document_tag.id
        """
        params = [
            list(folders.ids),
            list(documents.ids),  # using Postgresql's ANY() with a list to prevent empty list of documents
        ]
        self.env.cr.execute(query, params)
        result = self.env.cr.dictfetchall()

        # Translating result
        groups = self.env['viin_document.tag.cate'].browse({r['group_id'] for r in result})
        group_names = {group['id']: group['name'] for group in groups}

        tags = self.env['viin_document.tag'].browse({r['id'] for r in result})
        tags_names = {tag['id']: tag['name'] for tag in tags}

        for r in result:
            r['group_name'] = group_names.get(r['group_id'])
            r['display_name'] = tags_names.get(r['id'])

        return result
