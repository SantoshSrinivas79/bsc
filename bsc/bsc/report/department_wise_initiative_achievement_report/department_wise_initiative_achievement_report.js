// Copyright (c) 2016, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Department-wise Initiative Achievement Report"] = {
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
		},
		{
            		fieldname: 'month',
            		label: __('Month'),
            		fieldtype: 'MultiSelectList',
			get_data: function(txt) {
				return frappe.db.get_link_options('BSC Month', txt);
			},
       
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		value = $(`<span style='font-weight:bold'>${value}</span>`);
		var $value = $(value).css({"color":"black"});
		if (data.is_achieved=='Yes') {
			$value = $(value).css({"color":"green"});
		}
		else {
			$value = $(value).css({"color":"red"});
		}

		value = $value.wrap("<p></p>").parent().html();
		return value;
	},

};
