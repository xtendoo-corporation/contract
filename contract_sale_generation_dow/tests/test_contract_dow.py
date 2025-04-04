from datetime import date, timedelta

from freezegun import freeze_time

from odoo.tests.common import TransactionCase

from .common import ContractSaleDowCommon


class TestContractDow(ContractSaleDowCommon, TransactionCase):
    def _get_invoices_created_by_contract(self, day_offset):
        """
        Get the invoices created by the contract for a specific day of the week.

        :param day_offset:
            Number of days to add to the Monday (0 for Monday, 1 for Tuesday, etc.)

        :return:
            List of invoices created for the contract.
        """
        # Calculate the Monday of the current week
        monday = date.today() - timedelta(days=date.today().weekday())

        # Calculate the test date based on the offset
        test_day = monday + timedelta(days=day_offset)

        # Freeze the time to the test date
        with freeze_time(test_day):
            self.contract._cron_recurring_create(None, create_type="sale")
            invoices = self.env["sale.order"].search(
                [("origin", "=", self.contract.name)]
            )
        return invoices

    def test_recurring_invoice_creation_on_monday(self):
        invoices = self._get_invoices_created_by_contract(day_offset=0)
        self.assertTrue(
            invoices,
            "ERROR: Not invoice generated on Monday for the contract.",
        )

    def test_recurring_invoice_creation_on_tuesday(self):
        invoices = self._get_invoices_created_by_contract(day_offset=1)
        self.assertTrue(
            invoices,
            "ERROR: Not invoice generated on Tuesday for the contract.",
        )

    def test_recurring_invoice_creation_on_wednesday(self):
        invoices = self._get_invoices_created_by_contract(day_offset=3)
        self.assertFalse(
            invoices,
            "ERROR: Invoice generated on Wednesday for the contract.",
        )
