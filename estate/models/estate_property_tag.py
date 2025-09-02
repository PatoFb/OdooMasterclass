from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name asc"

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer()

    _sql_constraints = [
        ('estate_tag_name_uniq',
         'unique(name)',
         'The tag name must be unique.'),
    ]