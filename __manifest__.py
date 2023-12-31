{
    "name": "Product catalog",
    "version": "15.0.1.0.0",
    "category": "Services",
    "summary": """Product catalog to store and manage product data""",
    "license": "LGPL-3",
    "author": "Iva Boh",
    "maintainer": "https://github.com/IvaBoh",
    "website": "https://github.com/IvaBoh",
    "depends": ["base"],
    "data": [
        "security/product_catalog_groups.xml",
        "security/ir.model.access.csv",
        "security/product_catalog_security.xml",
        "views/product_catalog_menus.xml",
        "views/res_partner_views.xml",
        "views/res_company_views.xml",
        "views/product_attribute_views.xml",
        "views/product_attribute_value_views.xml",
        "views/product_category_views.xml",
        "views/product_product_views.xml",
        "views/supply_case_views.xml",
        "views/supply_item_views.xml",
        "wizard/update_product_qty_wizard_views.xml",
        "report/product_catalog_templates.xml",
        "report/product_catalog_reports.xml",
    ],
    "demo": [
        "data/res_partner_demo.xml",
        "data/res_company_demo.xml",
        "data/product_attribute_demo.xml",
        "data/product_attribute_value_demo.xml",
        "data/product_category_demo.xml",
        "data/product_product_demo.xml",
        "data/supply_item_demo.xml",
        "data/supply_case_demo.xml",
    ],
    "images": ["static/description/icon.png"],
    "support": "antutilo@gmail.com",
    "application": False,
    "installable": True,
    "auto_install": False,
}
