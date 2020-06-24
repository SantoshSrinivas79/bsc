
// Copyright (c) 2016, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.require("assets/bsc/js/kpi.js", function() {
frappe.query_reports["BSC Performance Report"] = {
	"filters": [
		{
            		fieldname: 'department',
            		label: __('Department'),
            		fieldtype: 'Link',
			options: 'Department'
		},
		{
            		fieldname: 'fiscal_year',
            		label: __('Fiscal Year'),
            		fieldtype: 'Link',
            		options: 'Fiscal Year',
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"reqd": 1
		},

	],
	"formatter": function(value, row, column, data, default_formatter) {

		if (column.fieldname=="bsc") {
			value = data.bsc_name;
			column.is_tree = true;
			if (data.indent==2) {
				column.link_onclick ="bsc.kpi.open_indicator(" + JSON.stringify(data) + ")";
			}
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
	"tree": true,
	"name_field": "bsc",
	"parent_field": "parent_bsc",
	"initial_depth": 0

}
});