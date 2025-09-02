from odoo import api, fields, models
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property Description"

    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Property Description', required=True, translate=True, default="Default Description")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected price $')
    selling_price = fields.Float('Selling price $', readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
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
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer received'),
            ('offer_accepted', 'Offer accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ], default='new', copy=False
    )
    property_type_id = fields.Many2one('estate.property.type', ondelete='set null')
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many('estate.property.offer', inverse_name='property_id',string='Offers')
    total_area = fields.Float(copmute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("total_area")
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends("best_price")
    def _compute_best_price(self):
        for estate in self:
            if estate.offer_ids:
                estate.best_price = max(estate.offer_ids.mapped("price"))
            else:
                estate.best_price = 0.0