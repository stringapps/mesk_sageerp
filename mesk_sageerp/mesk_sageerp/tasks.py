import os

import frappe
from frappe.utils import add_days , getdate, today
from frappe.utils.xlsxutils import make_xlsx
from erpnext.accounts.utils import get_fiscal_year



# def daily_export_sage_financial_statement():
# 	"""Export Sage Financial Statement report to Excel on the Desktop daily at 10 AM."""
# 	from mesk_sageerp.mesk_sageerp.report.sage_financial_statement.sage_financial_statement import (
# 		execute,
# 	)
# 	srs = frappe.get_single("Sage Report Setting")
# 	if not srs.enable_auto_creation_of_sfsr:
# 		return
	
# 	company = frappe.defaults.get_global_default("company")
# 	if not company:
# 		frappe.log_error("Sage Financial Statement Export: No default company set.")
# 		return
	
# 	desktop_path = os.path.expanduser(srs.folder_to_download_sfsr)
# 	os.makedirs(desktop_path, exist_ok=True)

# 	try:
# 		period_start_end_date = add_days(today(), -1)
# 		from_fiscal_year = frappe.db.get_value(
# 			"Fiscal Year",
# 			{"year_start_date": ("<=", getdate(period_start_end_date)), "year_end_date": (">=", getdate(period_start_end_date))},
# 			"name",
# 		)
# 		to_fiscal_year = frappe.db.get_value(
# 			"Fiscal Year",
# 			{"year_start_date": ("<=", getdate(period_start_end_date)), "year_end_date": (">=", getdate(period_start_end_date))},
# 			"name",
# 		)

# 		filters = frappe._dict(
# 			{
# 				"company": company,
# 				"filter_based_on": "Date Range",
# 				"period_start_date": period_start_end_date,
# 				"period_end_date": period_start_end_date,
# 				'presentation_currency': 'INR',
# 				"report": "Profit and Loss Statement",
# 				"include_default_book_entries": 1,
# 				'from_fiscal_year': from_fiscal_year,
# 				'to_fiscal_year': to_fiscal_year
# 			}
# 		)
# 		columns, data, *_ = execute(filters)
# 		# if not data:
# 		# 	return
# 		header = [col.get("label") for col in columns]
# 		rows = []
# 		for row in data:
# 			rows.append([row.get(col.get("fieldname"), "") for col in columns])

# 		xlsx_data = [header] + rows
# 		xlsx_file = make_xlsx(xlsx_data, "Sage Financial Statement")

# 		filename = f"{period_start_end_date}_SFSR.xlsx"
# 		filepath = os.path.join(desktop_path, filename)

# 		with open(filepath, "wb") as f:
# 			f.write(xlsx_file.getvalue())

# 		frappe.logger().info(f"Sage Financial Statement exported: {filepath}")

# 	except Exception:
# 		frappe.log_error(
# 			"Sage Financial Statement Export failed",
# 			frappe.get_traceback(),
# 		)


def daily_export_sage_trial_balance():
	"""Export Sage Trial Balance report to Excel on the Desktop daily at 10 AM."""
	from mesk_sageerp.mesk_sageerp.report.sage_trial_balance.sage_trial_balance import (
		execute,
	)
	srs = frappe.get_single("Sage Report Setting")
	if not srs.enable_auto_creation_of_sfsr:
		return
	
	company = frappe.defaults.get_global_default("company")
	
	if not company:
		frappe.log_error("Sage Trial Balance Export: No default company set.")
		return
	date = add_days(today(), -1)
	desktop_path = os.path.expanduser(srs.folder_to_download_sfsr)
	os.makedirs(desktop_path, exist_ok=True)

	try:

		filters = frappe._dict(
			{
				"company": company,
				"fiscal_year": get_fiscal_year(date, company=company)[0],
				"from_date": date,
				"to_date": date,
				'with_period_closing_entry_for_opening': 1,
				"with_period_closing_entry_for_current_period": 1,
				"include_default_book_entries": 1,
				"show_net_values": 1,
				"show_group_accounts": 1,
			}
		)
		columns, data, *_ = execute(filters)
		
		header = [col.get("label") for col in columns]
		rows = []
		for row in data:
			rows.append([row.get(col.get("fieldname"), "") for col in columns])

		xlsx_data = [header] + rows
		xlsx_file = make_xlsx(xlsx_data, "Sage Trial Balance")

		filename = f"{date}_STBR.xlsx"
		filepath = os.path.join(desktop_path, filename)

		with open(filepath, "wb") as f:
			f.write(xlsx_file.getvalue())

		frappe.logger().info(f"Sage Trial Balance exported: {filepath}")

	except Exception:
		frappe.log_error(
			"Sage Trial Balance Export failed",
			frappe.get_traceback(),
		)
