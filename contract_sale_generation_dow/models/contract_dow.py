from odoo import fields, models


class ContractDow(models.Model):
    """
    Esta clase permite almacenar los días de la semana.
    """

    _name = "contract.dow"
    _description = "Contract Days of the Week"

    name = fields.Char(string="Days of the Week", required=True)
    dow = fields.Integer(required=True)
