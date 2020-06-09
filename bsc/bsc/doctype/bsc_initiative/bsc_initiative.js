// Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt

frappe.ui.form.on('BSC Initiative', {
	setup: function(frm) {
		frm.fields_dict['bsc_initiative_assignment'].get_query = function () {
    			return {
    				filters: {
    					"docstatus": 2
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
		frm.fields_dict['department'].get_query = function () {
    			return {
    				filters: {
    					"is_group": 0,
    				}
    		   	}
		}
	},
	refresh: function(frm) {
		console.log('in refresh')
		if (frm.doc.docstatus == 0) {
			if(!frm.is_new()) {
				frm.page.clear_primary_action();
				frm.page.set_primary_action(__('Create Initiative Logs'), () => {
					frm.save('Submit');
				})
			}
		}

		/*if(frm.is_new() && frm.doc.initiative_months.length<12){
			frm.clear_table("initiative_months");
			var months = "Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec";
			var att_list = months.split(",");
                        att_list.forEach(function(month){
                            var child=cur_frm.add_child("initiative_months");
                            frappe.model.set_value(child.doctype,child.name,"month",month);
                            frm.refresh_field("initiative_months");
                        });
		}*/
	 },
	department: function(frm) {
		/*frm.set_value("bsc_indicator", "");
		frm.set_value("indicator_name", "");*/
	},
	employee: function(frm) {
		if(!frm.doc.employee)
			frm.set_value("employee_name", "");
	},
	validate: function(frm){
		console.log("in validate")

		frm.trigger("calc_time_total");		
		/*var total = 0;
		$.each(frm.doc.initiative_months || [], function(i, d) {
				total +=d.target;
		});
		frm.set_value("time_total", total);*/
	},
	initiative_name: function(frm){
		if (frm.doc.initiative_name && !frm.doc.description)
			frappe.model.set_value("description",frm.doc.initiative_name);
	},
	calc_time_total: function(frm){
		console.log("in calc")
		frm.set_value("time_total",frm.doc.jan+frm.doc.feb+frm.doc.mar+frm.doc.apr+frm.doc.may+frm.doc.jun+frm.doc.jul+frm.doc.aug+frm.doc.sep+frm.doc.oct+frm.doc.nov+frm.doc.dec);
	}

});
