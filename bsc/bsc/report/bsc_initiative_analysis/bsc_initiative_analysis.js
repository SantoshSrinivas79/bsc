// Copyright (c) 2016, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BSC Initiative Analysis"] = {
	"filters": [
		{
            		fieldname: 'department',
            		label: __('Department'),
            		fieldtype: 'Link',
			options: 'Department'
		},
		{
            		fieldname: 'bsc_perspective',
            		label: __('BSC Perspective'),
            		fieldtype: 'Link',
			options: 'BSC Perspective'       
		},
		{
            		fieldname: 'bsc_objective',
            		label: __('BSC Objective'),
            		fieldtype: 'Link',
			options: 'BSC Objective'       
		},
		{
            		fieldname: 'bsc_indicator',
            		label: __('BSC Indicator'),
            		fieldtype: 'Link',
			options: 'BSC Indicator'       
		},
		{
            		fieldname: 'bsc_month',
            		label: __('BSC Month'),
            		fieldtype: 'Link',
            		options: 'BSC Month'
		},
		{
            		fieldname: 'fiscal_year',
            		label: __('Fiscal Year'),
            		fieldtype: 'Link',
            		options: 'Fiscal Year',
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"reqd": 1
		},

	]
};
