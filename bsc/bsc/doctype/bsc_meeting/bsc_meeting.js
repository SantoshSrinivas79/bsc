// Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt

frappe.ui.form.on('BSC Meeting', {
	// refresh: function(frm) {

	// },
	 validate(frm) {
		var is_duplicate=0;
		$.each(frm.doc.members|| [], function(i, d) {
			$.each(frm.doc.members|| [], function(j, c) {
				if(i!=j){
					if(d.employee==c.employee){
						msgprint(__("You can not select same Employee ({0})",[d.employee]));
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
	bsc_committee: function(frm){
			console.log('is here'+frm.doc.members)
		var is_null=1;
		$.each(frm.doc.members|| [], function(i, d) {
			is_null=0;
		});
		if (is_null==1){
			console.log('is null')
			erpnext.utils.map_current_doc({
				method: "bsc.bsc.doctype.bsc_meeting.bsc_meeting.fetch_bsc_committee",
				source_name: frm.doc.bsc_committee,
				frm: frm
			});
		}
	}

});
