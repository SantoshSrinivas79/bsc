// Copyright (c) 2016, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Department-wise Target of Indicator"] = {
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
            		options: 'Fiscal Year'        
		},
		{
            		fieldname: 'bsc_indicator',
            		label: __('BSCIndicator'),
            		fieldtype: 'Link',
            		options: 'BSC Indicator'        
		}
	]
};
