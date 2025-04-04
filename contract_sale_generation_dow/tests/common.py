# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields


def to_date(date):
    return fields.Date.to_date(date)


class ContractSaleDowCommon:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "Contracts",
                "plan_id": cls.env.ref("analytic.analytic_plan_internal").id,
            }
        )
        cls.payment_term_id = cls.env.ref(
            "account.account_payment_term_end_following_month"
        )
        cls.fiscal_position_id = cls.env["account.fiscal.position"].create(
            {"name": "Contracts"}
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {"name": "pricelist for contract tests"}
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "partner tests contract",
                "property_product_pricelist": cls.pricelist.id,
                "property_payment_term_id": cls.payment_term_id.id,
                "property_account_position_id": cls.fiscal_position_id.id,
                "user_id": cls.env.user.id,
            }
        )
        cls.product_1 = cls.env.ref("product.product_product_1")
        cls.product_1.taxes_id += cls.env["account.tax"].search(
            [("type_tax_use", "=", "sale")], limit=1
        )
        cls.product_1.description_sale = "Test description sale"
        cls.line_template_vals = {
            "product_id": cls.product_1.id,
            "name": "Test Contract Template",
            "quantity": 1,
            "uom_id": cls.product_1.uom_id.id,
            "price_unit": 100,
            "discount": 50,
            "recurring_rule_type": "yearly",
            "recurring_interval": 1,
            "display_type": False,
        }
        cls.template_vals = {
            "name": "Test Contract Template",
            "contract_type": "sale",
            "contract_line_ids": [
                (0, 0, cls.line_template_vals),
            ],
        }
        cls.template = cls.env["contract.template"].create(cls.template_vals)
        # For being sure of the applied price
        cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.partner.property_product_pricelist.id,
                "product_id": cls.product_1.id,
                "compute_price": "formula",
                "base": "list_price",
            }
        )
        # Crear días de la semana.
        cls.dow_monday = cls.env["contract.dow"].create({"name": "Lunes", "dow": 0})
        cls.dow_tuesday = cls.env["contract.dow"].create({"name": "Martes", "dow": 1})

        cls.contract = cls.env["contract.contract"].create(
            {
                "name": "Test Contract",
                "partner_id": cls.partner.id,
                "pricelist_id": cls.partner.property_product_pricelist.id,
                "generation_type": "sale",
                "sale_autoconfirm": False,
                "date_start": "2020-01-15",
                "contract_type": "purchase",
                "contract_dow_ids": [(6, 0, [cls.dow_monday.id, cls.dow_tuesday.id])],
                "contract_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_1.id,
                            "name": "Services from #START# to #END#",
                            "quantity": 1,
                            "uom_id": cls.product_1.uom_id.id,
                            "price_unit": 100,
                            "discount": 50,
                            "recurring_rule_type": "monthly",
                            "recurring_interval": 1,
                            "date_start": "2018-02-15",
                            "recurring_next_date": "2018-02-22",
                            "display_type": False,
                        },
                    )
                ],
            }
        )
