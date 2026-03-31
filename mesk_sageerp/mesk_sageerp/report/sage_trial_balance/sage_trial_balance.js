// Copyright (c) 2026, D-codE and contributors
// For license information, please see license.txt

frappe.query_reports["Sage Trial Balance"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
			reqd: 1,
			read_only: 1,
			on_change: function (query_report) {
				var fiscal_year = query_report.get_values().fiscal_year;
				if (!fiscal_year) {
					return;
				}
				frappe.model.with_doc("Fiscal Year", fiscal_year, function (r) {
					var fy = frappe.model.get_doc("Fiscal Year", fiscal_year);
					frappe.query_report.set_filter_value({
						from_date: fy.year_start_date,
						to_date: fy.year_end_date,
					});
				});
			},
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: erpnext.utils.get_fiscal_year(frappe.datetime.get_today(), true)[1],
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: erpnext.utils.get_fiscal_year(frappe.datetime.get_today(), true)[2],
		},
		{
			fieldname: "cost_center",
			label: __("Cost Center"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options("Cost Center", txt, {
					company: frappe.query_report.get_filter_value("company"),
				});
			},
			options: "Cost Center",
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options("Project", txt, {
					company: frappe.query_report.get_filter_value("company"),
				});
			},
			options: "Project",
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "finance_book",
			label: __("Finance Book"),
			fieldtype: "Link",
			options: "Finance Book",
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "presentation_currency",
			label: __("Currency"),
			fieldtype: "Select",
			options: erpnext.get_presentation_currency_list(),
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "with_period_closing_entry_for_opening",
			label: __("With Period Closing Entry For Opening Balances"),
			fieldtype: "Check",
			default: 1,
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "with_period_closing_entry_for_current_period",
			label: __("Period Closing Entry For Current Period"),
			fieldtype: "Check",
			default: 1,
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "show_zero_values",
			label: __("Show zero values"),
			fieldtype: "Check",
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "show_unclosed_fy_pl_balances",
			label: __("Show unclosed fiscal year's P&L balances"),
			fieldtype: "Check",
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "include_default_book_entries",
			label: __("Include Default FB Entries"),
			fieldtype: "Check",
			default: 1,
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "show_net_values",
			label: __("Show net values in opening and closing columns"),
			fieldtype: "Check",
			default: 1,
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "show_group_accounts",
			label: __("Show Group Accounts"),
			fieldtype: "Check",
			default: 1,
			read_only: 1,
			hidden: 1
		},
	],
	onload: function () {
		frappe.query_report.page.add_inner_button(__("Export to Excel"), function () {
			let filters = frappe.query_report.get_filter_values();
			frappe.call({
				method: "mesk_sageerp.mesk_sageerp.report.sage_trial_balance.sage_trial_balance.export_to_excel",
				args: { filters: filters },
				freeze: true,
				freeze_message: __("Exporting to Excel..."),
				callback: function (r) {
					if (r.message) {
						frappe.msgprint(__("Excel file saved to: {0}", [r.message]));
					}
				},
			});
		}).addClass("btn-primary");
	}
};
erpnext.utils.add_dimensions("Sage Trial Balance", 6);