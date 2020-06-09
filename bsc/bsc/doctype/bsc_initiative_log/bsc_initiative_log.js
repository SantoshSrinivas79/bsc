// Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt

frappe.ui.form.on('BSC Initiative Log', {
	setup: function(frm) {
		frm.fields_dict['department'].get_query = function () {
    			return {
    				filters: {
    					"is_group": 0,
    				}
    		   	}
		}

		frm.fields_dict['bsc_initiative'].get_query = function () {
    			return {
    				filters: {
    					"docstatus": 2
    				}
    		   	}
		}
		frm.trigger("func_mandatories");		
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
		/*if(frm.doc.department && frm.doc.bsc_indicator && frm.doc.bsc_initiative){
			frappe.call({
  				method: 'bsc.bsc.doctype.bsc_indicator.bsc_indicator.get_month_by_indicator', 
				args: {
					"department": frm.doc.department,
					"bsc_indicator": frm.doc.bsc_indicator,
					"doctype": frm.doc.doctype,
					"bsc_initiative": frm.doc.bsc_initiative
				}
			}).done((r) => {
				console.log('in done'+r.message)
				console.log('in done'+r.message)
				frm.set_df_property("month", "options", r.message);
			}).fail((f) => {
				msgprint(__('No Months for this Department and Indicator'));
			});
		}*/	
	},
	department: function(frm) {
		/*frm.set_value("indicator_name", "");
		frm.set_value("bsc_initiative", "");*/
	},
	bsc_indicator: function(frm) {
		/*frm.set_value("bsc_initiative", "");*/
	},
	bsc_initiative: function(frm) {
		frm.trigger("func_months");		
	},
	is_achieved: function(frm) {
		frm.trigger("func_mandatories");		
	},
	func_mandatories: function(frm){
		frappe.call({
                	"method": "frappe.client.get",
                	args: {
                    		doctype: "BSC Settings"
                	},
                	callback: function (data) {
				if(frm.doc.is_achieved=='Yes'){
					frm.toggle_reqd("weakness_reasons", 0);
					frm.toggle_reqd("suggested_solutions", 0);
					frm.toggle_reqd("evidence_attachment", data.message.evidence_mandatory);
				}else if(frm.doc.is_achieved=='No'){
					frm.toggle_reqd("weakness_reasons", data.message.weakness_mandatory);
					frm.toggle_reqd("suggested_solutions", data.message.suggested_mandatory);
					frm.toggle_reqd("evidence_attachment", 0);
				}
            	}})

	}




});
