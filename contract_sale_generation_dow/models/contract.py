import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ContractContract(models.Model):
    _inherit = "contract.contract"

    dow_ids = fields.Many2many("contract.dow", string="Days of the Week")
