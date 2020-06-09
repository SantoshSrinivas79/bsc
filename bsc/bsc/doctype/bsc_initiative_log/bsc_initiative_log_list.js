frappe.listview_settings['BSC Initiative Log'] = {
	add_fields: ['docstatus','is_achieved'],
	get_indicator: function(doc) {
		const color = {
				'Yes': 'green',
				'No': 'red'
			};
		return [__(doc.is_achieved), color[doc.is_achieved], "is_achieved,=," + doc.is_achieved];
		
	}
}
