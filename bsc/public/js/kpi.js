frappe.provide("bsc.bsc_performance_report");

bsc.kpi = {
	"filters": get_filters(),
	"formatter": function(value, row, column, data, default_formatter) {

		if (column.fieldname=="bsc") {
			value = data.bsc_name;
			column.is_tree = true;
				column.link_onclick ="bsc.kpi.open_indicator(" + JSON.stringify(data) + ")";
			}

		value = default_formatter(value, row, column, data);
		if (!data.parent_bsc) {
			value = $(`<span>${value}</span>`);

			var $value = $(value).css("font-weight", "bold");
			if (data.warn_if_negative && data[column.fieldname] < 0) {
				$value.addClass("text-danger");
			}

			value = $value.wrap("<p></p>").parent().html();
		}
		if (!data.width) {
			return '';
		}

		return value;
	},
	"open_indicator": function(data) {
		console.log(data)
		if (!data.bsc) return;
		var bsc_indicator= $.grep(frappe.query_report.filters, function(e){ return e.df.fieldname == 'bsc_indicator'; })
		console.log(data.bsc)

		frappe.route_options = {
			"bsc_indicator": data.bsc,
			"fiscal_year": data.fiscal_year
		};
		frappe.set_route("query-report", "Department-wise Indicator Performance");
	},
	"tree": true,
	"name_field": "account",
	"parent_field": "parent_account",
	"initial_depth": 3,
	onload: function(report) {
		// dropdown for links to other financial statements
		erpnext.financial_statements.filters = get_filters()

		report.page.add_inner_button(__("Balance Sheet"), function() {
			var filters = report.get_values();
			frappe.set_route('query-report', 'Balance Sheet', {company: filters.company});
		}, __('Financial Statements'));
		report.page.add_inner_button(__("Profit and Loss"), function() {
			var filters = report.get_values();
			frappe.set_route('query-report', 'Profit and Loss Statement', {company: filters.company});
		}, __('Financial Statements'));
		report.page.add_inner_button(__("Cash Flow Statement"), function() {
			var filters = report.get_values();
			frappe.set_route('query-report', 'Cash Flow', {company: filters.company});
		}, __('Financial Statements'));
	}
};

function get_filters(){
	let filters = [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"finance_book",
			"label": __("Finance Book"),
			"fieldtype": "Link",
			"options": "Finance Book"
		},
		{
			"fieldname":"from_fiscal_year",
			"label": __("Start Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"reqd": 1
		},
		{
			"fieldname":"to_fiscal_year",
			"label": __("End Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"reqd": 1
		},
		{
			"fieldname": "periodicity",
			"label": __("Periodicity"),
			"fieldtype": "Select",
			"options": [
				{ "value": "Monthly", "label": __("Monthly") },
				{ "value": "Quarterly", "label": __("Quarterly") },
				{ "value": "Half-Yearly", "label": __("Half-Yearly") },
				{ "value": "Yearly", "label": __("Yearly") }
			],
			"default": "Yearly",
			"reqd": 1
		},
		// Note:
		// If you are modifying this array such that the presentation_currency object
		// is no longer the last object, please make adjustments in cash_flow.js
		// accordingly.
		{
			"fieldname": "presentation_currency",
			"label": __("Currency"),
			"fieldtype": "Select",
			"options": erpnext.get_presentation_currency_list()
		},
		{
			"fieldname": "cost_center",
			"label": __("Cost Center"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Cost Center', txt, {
					company: frappe.query_report.get_filter_value("company")
				});
			}
		}
	]

	erpnext.dimension_filters.forEach((dimension) => {
		filters.push({
			"fieldname": dimension["fieldname"],
			"label": __(dimension["label"]),
			"fieldtype": "Link",
			"options": dimension["document_type"]
		});
	});

	return filters;
}


