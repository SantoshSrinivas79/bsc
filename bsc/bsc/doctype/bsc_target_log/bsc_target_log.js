// Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt

frappe.ui.form.on('BSC Target Log', {
	setup: function(frm) {	
		frm.fields_dict['department'].get_query = function () {
    			return {
    				filters: {
    					"is_group": 0,
    				}
    		   	}
		}
		frm.fields_dict['bsc_target'].get_query = function () {
    			return {
    				filters: {
    					"docstatus": 2,
    				}
    		   	}
		}		
		frm.set_query("bsc_indicator", function() {
			return {
				query: "bsc.bsc.doctype.bsc_indicator.bsc_indicator.get_indicator_by_department",
				filters: {
					department: frm.doc.department
				}
			};
		});
	},
	func_months: function(frm){
		if(frm.doc.department && frm.doc.bsc_indicator){
			frappe.call({
  				method: 'bsc.bsc.doctype.bsc_indicator.bsc_indicator.get_month_by_indicator', 
				args: {
					"department": frm.doc.department,
					"bsc_indicator": frm.doc.bsc_indicator,
					doctype:frm.doc.doctype,
					bsc_initiative:""
				}
			}).done((r) => {
				console.log('in done'+r.message)
				console.log('in done'+r.message.months)
				frm.set_df_property("month", "options", r.message);
			}).fail((f) => {
				msgprint(__('No Months for this Department and Indicator'));
			});
		}	
	},
	department: function(frm) {
		frm.set_value("indicator_name", "");
	},
	bsc_indicator: function(frm) {
		frm.trigger("func_months");		
	},
	validate: function(frm){
		frm.trigger("calc_target");
		/*if(frm.doc.achieved && frm.doc.target){
			frm.set_value("target_log_percent", frm.doc.achieved/frm.doc.target*100);
		}*/
	},
	clac_target: function(frm){
		if(frm.doc.target==0){
			frappe.call({
		            method: "frappe.client.get",
		             args: {
		                doctype: "BSC Target",
		                name: frm.doc.bsc_target
		            },
            		callback: function (data) {
				if(frm.doc.month == 'Jan')
					frm.set_value("target", data.message.jan);
				else if(frm.doc.month == 'Feb')
					frm.set_value("target", data.message.feb);
				else if(frm.doc.month == 'Mar')
					frm.set_value("target", data.message.mar);
				else if(frm.doc.month == 'Apr')
					frm.set_value("target", data.message.apr);
				else if(frm.doc.month == 'May')
					frm.set_value("target", data.message.may);
				else if(frm.doc.month == 'Jun')
					frm.set_value("target", data.message.jun);
				else if(frm.doc.month == 'Jul')
					frm.set_value("target", data.message.jul);
				else if(frm.doc.month == 'Aug')
					frm.set_value("target", data.message.aug);
				else if(frm.doc.month == 'Sep')
					frm.set_value("target", data.message.sep);
				else if(frm.doc.month == 'Oct')
					frm.set_value("target", data.message.oct);
				else if(frm.doc.month == 'Nov')
					frm.set_value("target", data.message.nov);
				else if(frm.doc.month == 'Dec')
					frm.set_value("target", data.message.dec);
			}})	
		}			
	}


});
