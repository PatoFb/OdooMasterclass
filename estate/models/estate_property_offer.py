from odoo import api, fields, models
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ], copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("date_deadline")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = offer.create_date or fields.Date.today()
            offer.date_deadline = base_date + relativedelta(days=offer.validity)

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for offer in self:
            base_date = offer.create_date or fields.Date.today()
            offer.validity = (offer.date_deadline - base_date).days