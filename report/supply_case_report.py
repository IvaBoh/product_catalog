from odoo import api, models, _


class SupplyCaseReport(models.AbstractModel):
    """
    This class is called before report creation.
    It allows to add custom info without usage of wizards.
    """

    _name = "report.product_catalog.supply_case_report_template"
    _description = _("Report on supply cases of products")

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        This method is essential. It allows to add custom date to report.
        One could also save some date form several models to some wizard
        before returning the data, so a complex report could be created
        """
        report = self.env["ir.actions.report"]._get_report_from_name(
            "product_catalog.supply_case_report_template"
        )
        records = self.env[report.model].browse(docids)
        company = self.env.user.company_id
        return {
            "docs": records,
            "company": company,
        }
