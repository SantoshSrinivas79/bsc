// Copyright (c) 2016, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Department-wise Indicator Performance"] = {
	"filters": [
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
            		label: __('BSC Month'),
            		fieldtype: 'MultiSelectList',
			get_data: function(txt) {
				return frappe.db.get_link_options('BSC Month', txt);
			},       
		},
		{
            		fieldname: 'department',
            		label: __('Department'),
            		fieldtype: 'MultiSelectList',
			get_data: function(txt) {
				return frappe.db.get_link_options('Department', txt);
			},        
		},
		{
            		fieldname: 'bsc_indicator',
            		label: __('BSC Indicator'),
            		fieldtype: 'Link',
            		options: 'BSC Indicator',
			"get_query": function() {
				var vari = frappe.query_report.get_filter_value('bsc_objective');
				if (vari){
					return {
						"doctype": "BSC Indicator",
						"filters": {
							"bsc_objective": vari ,
						}
					}
				}
			}

		},
		{
            		fieldname: 'bsc_perspective',
            		label: __('BSC Perspective'),
            		fieldtype: 'Link',
            		options: 'BSC Perspective',
			on_change: function() {
				frappe.query_report.set_filter_value('bsc_objective', "");
				frappe.query_report.set_filter_value('bsc_indicator', "");
			}
		},
		{
            		fieldname: 'bsc_objective',
            		label: __('BSC Objective'),
            		fieldtype: 'Link',
            		options: 'BSC Objective',
			on_change: function() {
				frappe.query_report.set_filter_value('bsc_indicator', "");
			},
			"get_query": function() {
				var vari = frappe.query_report.get_filter_value('bsc_perspective');
				if (vari){
					return {
						"doctype": "BSC Objective",
						"filters": {
							"bsc_perspective": vari ,
						}
					}
				}
			}
		},
		{
            		fieldname: 'greater',
            		label: __('Achieved Greater than Target'),
            		fieldtype: 'Check',
			"default": 0
		},
		{
            		fieldname: 'chart_type',
            		label: __('Chart Type'),
            		fieldtype: 'Select',
			"options": ["Line", "Bar"],
			"default": "Bar"
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		value = $(`<span style='font-weight:bold'>${value}</span>`);
		var $value = $(value).css({"color":"black"});
		if (data.percent>=0.00 && data.percent<50.00) {
			$value = $(value).css({"color":"red"});
		}
		else if (data.percent>=50.00 && data.percent<80.00) {
			$value = $(value).css({"color":"blue"});
		}
		else {
			$value = $(value).css({"color":"green"});
		}

		value = $value.wrap("<p></p>").parent().html();
		return value;
	},
};
