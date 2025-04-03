from datetime import date, timedelta

from freezegun import freeze_time

from odoo.tests.common import TransactionCase

from .common import ContractSaleDowCommon


class TestContractDow(ContractSaleDowCommon, TransactionCase):
    def _create_contract_line_and_run_test(self, day_offset, expected_invoice=True):
        """
        Create a contract line and run the test for invoice creation on a specific date.

        :param day_offset:
            Number of days to add to the Monday (0 for Monday, 1 for Tuesday, etc.)
        :param expected_invoice:
            Boolean indicating if an invoice is expected (True) or not (False)
        """
        contrato = self.contract

        # Se crea una línea de contrato lista para la generación en el día especificado
        self.env["contract.line"].create(
            {
                "contract_id": contrato.id,
                "name": f'Servicio semanal '
                f'{["lunes", "martes", "miércoles"][day_offset]}',
                "product_id": self.product_1.id,
                "quantity": 1,
                "recurring_rule_type": "weekly",
                "recurring_interval": 1,
                "date_start": date.today() - timedelta(days=7),
                "recurring_next_date": date.today() - timedelta(days=6),
            }
        )

        # Calcular el lunes de la semana actual
        hoy = date.today()
        lunes = hoy - timedelta(days=hoy.weekday())

        # Calcular el día correspondiente sumando el offset al lunes
        test_day = lunes + timedelta(days=day_offset)

        # Congelar el tiempo en la fecha de prueba.
        with freeze_time(test_day):
            contrato._cron_recurring_create()
            facturas = self.env["account.move"].search(
                [("invoice_origin", "=", contrato.name)]
            )
            if expected_invoice:
                self.assertTrue(
                    facturas,
                    f"No se generó factura en "
                    f"{['lunes', 'martes', 'miércoles'][day_offset]}"
                    f" para el contrato.",
                )
            else:
                self.assertFalse(
                    facturas,
                    f"Se generó factura en "
                    f"{['lunes', 'martes', 'miércoles'][day_offset]}"
                    f" para el contrato.",
                )

    def test_recurring_invoice_creation_on_monday(self):
        self._create_contract_line_and_run_test(day_offset=0)

    def test_recurring_invoice_creation_on_tuesday(self):
        self._create_contract_line_and_run_test(day_offset=1)

    def test_recurring_invoice_creation_on_wednesday(self):
        self._create_contract_line_and_run_test(day_offset=2, expected_invoice=False)
