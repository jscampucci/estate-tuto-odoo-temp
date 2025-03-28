from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    price = fields.Float("Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        "Status",
        default="draft",
        copy=False,
    )
