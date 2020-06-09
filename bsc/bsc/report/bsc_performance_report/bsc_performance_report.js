// Copyright (c) 2016, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.require("assets/erpnext/js/financial_statements.js", function() {

frappe.query_reports["BSC Performance Report"] = {
	"filters": [
		{
            		fieldname: 'department',
            		label: __('Department'),
            		fieldtype: 'Link',
			options: 'Department'
		},
		{
            		fieldname: 'bsc_indicator',
            		label: __('BSC Indicator'),
            		fieldtype: 'Link',
			options: 'BSC Indicator'       
		},
		{
            		fieldname: 'bsc_initiative',
            		label: __('BSC Iniviative'),
            		fieldtype: 'Link',
			options: 'BSC Iniviative'       
		},
		{
            		fieldname: 'fiscal_year',
            		label: __('Fiscal Year'),
            		fieldtype: 'Link',
            		options: 'Fiscal Year',
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"reqd": 1
		}

	],
	"formatter": function(value, row, column, data, default_formatter) {

		if (column.fieldname=="bsc") {
			value = data.bsc_name;

			column.link_onclick =
				"erpnext.financial_statements.open_general_ledger(" + JSON.stringify(data) + ")";
			column.is_tree = true;
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
       		if (column.fieldname == "perc") {
			console.log('in perc')
            		value = "<span style='text-align:center'>" + value + "</span>";
			var $value = $(value).css("text-align", "left");

			value = $value.wrap("<p></p>").parent().html();

        	}
		return value;
	},

	"tree": true,
	"name_field": "bsc",
	"parent_field": "parent_bsc",
	"initial_depth": 0

}
});