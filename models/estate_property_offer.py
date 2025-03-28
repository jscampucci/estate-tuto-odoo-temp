from odoo import models, fields, api
import datetime


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
    validity = fields.Integer("Validity (in days)", default=7)
    create_date = fields.Date(
        "Creation Date", readonly=True, default=fields.Datetime.now
    )
    date_deadline = fields.Date(
        "Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

    @api.depends("create_date", "validity", "date_deadline")
    def _compute_deadline(self):
        for rec in self:
            if rec.create_date:
                create_date = fields.Datetime.from_string(rec.create_date)
                rec.date_deadline = create_date + datetime.timedelta(days=rec.validity)
            else:
                rec.date_deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.date_deadline and rec.create_date:
                create_date = fields.Date.from_string(rec.create_date)
                rec.validity = (rec.date_deadline - create_date).days
            else:
                rec.validity = 0
