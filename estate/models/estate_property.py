from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property Description"

    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Property Description', required=True, translate=True)
    price = fields.Float('Price $', required=True)
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