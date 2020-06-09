// Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt

frappe.ui.form.on('BSC Indicator', {
	refresh: function(frm) {

		if (frm.doc.docstatus == 0 && !frm.is_new()) {
			if ((frm.doc.departments || []).length) {
				frm.add_custom_button(__("Create Targets and Initiative Assignments"),
					function() {
						frm.events.create_targets_and_initiatives_assignments(frm);
					}
				).toggleClass('btn-primary', !(frm.doc.departments || []).length);
			}
		}

	},
	create_targets_and_initiatives_assignments: function (frm) {
		return frappe.call({
			doc: frm.doc,
			method: 'create_targets_and_initiatives_assignments',
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
	}

});
