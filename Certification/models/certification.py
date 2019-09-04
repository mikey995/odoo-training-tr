from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Certification(models.Model):
    _name = 'certification'
    _description = "Certification"

    number = fields.Char()
    date = fields.Date(string="Validation Date")
    description = fields.Text(string="Validation Details")
    '''
        standard_id, id kelimesi certification'in başka bir model
        tablosuna bağlantılı olduğunu gösteriyor.
    '''

    '''
        Veri tabanımıza baktığımız zaman 3 adet bağlantılı alan ile ilgili
        integer alan görmemiz gerekiyor.
    '''
    standard_id = fields.Many2one("certification.standard")
    #bir kişi birden fazla sertifikası olabilir, bir sertifika bir kişiye ait olabilir.
    #sertifikanın sahibi
    owner_id = fields.Many2one("res.partner")
    #entity = sertifikayı veren kişi
    entity_id = fields.Many2one("res.partner")

    expiry_days = fields.Integer('Expiry Days', readonly=True, compute='_compute_expiry_days')
    expiry_status = fields.Selection([
        ('expired', "Expired"),
        ('available', "Available")
    ], readonly=True, compute='_compute_expiry_days', store=True)

    @api.constrains('entity_id')
    def _check_entity_id(self):
        if self.entity_id and self.entity_id.is_certification_body == False:
            raise ValidationError('It is not a certification entity')

    @api.depends('date')
    def _compute_expiry_days(self):
        for certificate in self:
            if certificate.date:
              certificate.expiry_days = (certificate.date - fields.Date.today()).days
              if certificate.expiry_days > 0:
                  certificate.expiry_status = "available"
              else:
                  certificate.expiry_status = "expired"

    @api.multi
    def update_date_one_month(self):
        self.ensure_one()
        if self.date:
            self.write({'date': self.date + timedelta(days=30)})

