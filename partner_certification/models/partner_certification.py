from odoo import models, fields, api

class PartnerCertification(models.Model):
    _name = "partner.certification"

    name = fields.Many2one("res.partner")

    type = fields.Selection([
        ('passport', "Passport"),
        ('id_card', "ID Card"),
        ('driving_license', "Driving License")
    ],)

    id_number = fields.Char(string="Identification Number")