// Copyright (c) 2016, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BSC Report 01"] = {
	"filters": [
		{
            		fieldname: 'department',
            		label: __('Department'),
            		fieldtype: 'MultiSelectList',
			get_data: function(txt) {
				return frappe.db.get_link_options('Department', txt);
			},
        
		},
		{
            		fieldname: 'fiscal_year',
            		label: __('Fiscal Year'),
            		fieldtype: 'Link',
            		options: 'Fiscal Year',
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"reqd": 1
		},
		{
            		fieldname: 'bsc_indicator',
            		label: __('BSCIndicator'),
            		fieldtype: 'MultiSelectList',
			get_data: function(txt) {
				return frappe.db.get_link_options('BSC Indicator', txt);
			},
       
		},
		{
            		fieldname: 'bsc_month',
            		label: __('BSCMonth'),
            		fieldtype: 'MultiSelectList',
			get_data: function(txt) {
				return frappe.db.get_link_options('BSC Month', txt);
			},
       
		}

	]
};
