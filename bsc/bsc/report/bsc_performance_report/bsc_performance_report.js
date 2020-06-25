
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
	"formatter": bsc.kpi.formatter,
	"tree": true,
	"name_field": "bsc",
	"parent_field": "parent_bsc",
	"initial_depth": 0

}
});