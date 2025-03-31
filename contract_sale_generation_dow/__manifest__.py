{
    "name": "Contract Sale Generation with Day of Week",
    "version": "18.0.1.0.0",  # Cambiado a un formato correcto de versión
    "category": "Contract Management",
    "author": "Xtendoo Software S.L., Odoo Community Association (OCA)",  # Agregado OCA
    "license": "AGPL-3",  # Añadido tipo de licencia compatible
    "website": "https://github.com/OCA/contract",
    "depends": ["contract_sale_generation"],
    "data": [
        "data/contract_dow.xml",
        "views/contract_dow.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}
