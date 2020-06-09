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
	"formatter": erpnext.financial_statements.formatter,
	"tree": true,
	"name_field": "account",
	"parent_field": "parent_account",
	"initial_depth": 3

}
});