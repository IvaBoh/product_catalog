from odoo import api, models, _


class SupplyCaseReport(models.AbstractModel):
    _name = "report.product_catalog.supply_case_report_template"
    _description = _("Report on supply cases of products")

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env["ir.actions.report"]._get_report_from_name(
            "product_catalog.supply_case_report_template"
        )
        records = self.env[report.model].browse(docids)
        company = self.env.user.company_id
        return {
            "docs": records,
            "company": company,
        }
