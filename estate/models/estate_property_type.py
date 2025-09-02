from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char('Type Name', required=True, translate=True)
    property_ids = fields.One2many('estate.property', inverse_name='property_type_id', string='Properties')

    _sql_constraints = [
        ('estate_type_name_uniq',
         'unique(name)',
         'The type name must be unique.'),
    ]