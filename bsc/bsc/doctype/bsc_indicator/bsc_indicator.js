// Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt

frappe.ui.form.on('BSC Indicator', {
	refresh: (frm)=>{
		if(!frm.is_new()) {
			frm.add_custom_button(__('Assign Department'), function () {
				frm.trigger("assign_department");
			});
		}

		if (frm.doc.docstatus == 0 && !frm.is_new()) {
			if ((frm.doc.departments || []).length) {
				frm.add_custom_button(__("Create Indicator Assignments"),
					function() {
						frm.events.create_indicator_assignments(frm);
					}
				).toggleClass('btn-primary', !(frm.doc.departments || []).length);
			}
		}

	},
	create_indicator_assignments: function (frm) {
		return frappe.call({
			doc: frm.doc,
			method: 'create_indicator_assignments',
			callback: function(r) {
				if (r.docs[0].departments){
					frm.save();
					frm.refresh();
				}
			}
		})
	},
	setup: function(frm){
		cur_frm.set_query("department", "departments", function(doc, cdt, cdn) {
	        var d = locals[cdt][cdn];
	        return{
    		    filters: [
    		        ['Department', 'is_group', '=',0]
    		    ]}		        
		});
	},
	 validate(frm) {
		var is_duplicate=0;
		$.each(frm.doc.departments || [], function(i, d) {
			$.each(frm.doc.departments || [], function(j, c) {
				if(i!=j){
					if(d.department==c.department){
						msgprint(__("You can not select same Department ({0})",[d.department]));
						frappe.validated = false;
						is_duplicate=1;
						return false;
					}
				}              		
			});
			if(is_duplicate==1){
				return false;
			}
		});
	},
	assign_department: function(frm) {
		var d = new frappe.ui.Dialog({
			title: __('Assign Department'),
			fields: [
				{
					"label": __("Department"),
					"fieldname": "department",
					"fieldtype": "Select",
					"options": frm.doc.departments.map(d => d.department),
					"reqd": 1
				},
				{
					"label": __("Fiscal Year"),
					"fieldname": "fiscal_year",
					"fieldtype": "Link",
					"options": "Fiscal Year",
					"reqd": 1,
					"default": frappe.defaults.get_user_default("fiscal_year"),
				}
			],
			primary_action: function() {
				var data = d.get_values();

				frappe.call({
					doc: frm.doc,
					method: "assign_department",
					args: data,
					callback: function(r) {
						if(!r.exc) {
							d.hide();
							frm.reload_doc();
						}
					}
				});
			},
			primary_action_label: __('Assign')
		});
		d.show();
	}


});
