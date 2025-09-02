from odoo import api, fields, models, exceptions
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

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            base = offer.create_date or fields.Datetime.now()
            base_date = fields.Date.to_date(base)
            offer.date_deadline = base_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            base = offer.create_date or fields.Datetime.now()
            base_date = fields.Date.to_date(base)
            offer.validity = (offer.date_deadline - base_date).days

    def accept_offer(self):
        if self.property_id.state == "offer_accepted":
            exceptions.UserError("Cannot accept more than one offer")
        else:
            self.status = "accepted"
            self.property_id.partner_id = self.partner_id
            self.property_id.selling_price = self.price
            self.property_id.state = "offer_accepted"

    def refuse_offer(self):
        self.status = "refused"