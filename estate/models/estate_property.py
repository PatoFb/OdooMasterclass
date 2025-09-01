from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property Description"

    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Property Description', required=True, translate=True)
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float('Expected price $', required=True)
    selling_price = fields.Float('Selling price $', required=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Float()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    active = fields.Boolean('Active', default=True)
    address = fields.Text('Property Address', required=True)
    type = fields.Selection(
        selection=[
         ("apartment", "Property is an apartment"),
         ("house", "Property is a house"),
      ],
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', 'The price can\'t be negative.'),
    ]