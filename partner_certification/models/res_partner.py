from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    names = fields.One2many("partner.certification", "name", string="Employee Name")