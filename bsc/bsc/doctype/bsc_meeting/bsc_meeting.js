// Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt

frappe.ui.form.on('BSC Meeting', {
	// refresh: function(frm) {

	// },
	 validate(frm) {
		var is_duplicate=0;
		$.each(frm.doc.meeting_attendance|| [], function(i, d) {
			$.each(frm.doc.meeting_attendance|| [], function(j, c) {
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
	}

});
