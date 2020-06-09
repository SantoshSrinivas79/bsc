frappe.listview_settings['BSC Target Log'] = {
	onload: function(me) {
		var months = {
			1: "Jan",
			2: "Feb",
			3: "Mar",
			4: "Apr",
			5: "May",
			6: "Jun",
			7: "Jul",
			8: "Aug",
			9: "Sep",
			10: "Oct",
			11: "Nov",
			12: "Dec"
		};
		var month_date = new Date(frappe.datetime.nowdate())
		var mo=months[(month_date.getMonth()+1)]
		frappe.route_options["docstatus"]=0
		frappe.route_options["month"]=mo
		frappe.route_options["fiscal_year"]=frappe.defaults.get_user_default("fiscal_year")
	}
}
