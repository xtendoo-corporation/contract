from odoo import fields, models


class ContractDow(models.Model):
    """
    This class allows to store the days of the week.
    """

    _name = "contract.dow"
    _description = "Contract Days of the Week"

    name = fields.Char(string="Days of the week", required=True)
    dow = fields.Integer(required=True)
