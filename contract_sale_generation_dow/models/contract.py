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
        _logger.info("domain del super: %s", domain)

        # Obtener el día de la semana actual (0 = Lunes, 1 = Martes, ..., 6 = Domingo).
        today_weekday = datetime.now().weekday()

        # Filtrar contratos que contienen el día actual.
        domain.append("|")
        domain.append(("contract_dow_ids.dow", "=", today_weekday))
        domain.append(("contract_dow_ids", "=", False))

        _logger.info("domain retornado: %s", domain)
        return domain
