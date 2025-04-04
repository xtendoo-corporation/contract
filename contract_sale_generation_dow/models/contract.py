import logging
from datetime import datetime

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ContractContract(models.Model):
    _inherit = "contract.contract"

    contract_dow_ids = fields.Many2many(
        comodel_name="contract.dow",
        string="Days of the Week",
        help="Days of the week when the contract should generate orders.",
    )

    @api.model
    def _get_contracts_to_invoice_domain(self, date_ref=None):
        domain = super()._get_contracts_to_invoice_domain(date_ref)

        # Get the current weekday (0 = Monday, 1 = Tuesday, ..., 6 = Sunday).
        today_weekday = datetime.now().weekday()

        # Filter contracts that contain the current day.
        domain.append("|")
        domain.append(("contract_dow_ids.dow", "=", today_weekday))
        domain.append(("contract_dow_ids", "=", False))
        return domain
