// Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
// For license information, please see license.txt

frappe.ui.form.on('BSC Target', {
	refresh: function(frm) {
		if (frm.doc.docstatus == 0) {
			if(!frm.is_new()) {
				frm.page.clear_primary_action();
				frm.page.set_primary_action(__('Create Target Logs'), () => {
					frm.save('Submit');
				})
			}
		}
	 },
	onload: function(frm){
		frm.trigger("change_properties");		
	},
	setup: function(frm) {
		frm.fields_dict['department'].get_query = function () {
    			return {
    				filters: {
    					"is_group": 0,
    				}
    		   	}
		}

		frm.set_df_property('target',  'read_only',  frm.doc.uom=='Cumulative'? 1 : 0);

		/*frm.set_query("bsc_indicator", function() {
			return {
				query: "bsc.bsc.doctype.bsc_indicator.bsc_indicator.get_indicator_by_department",
				filters: {
					department: frm.doc.department
				}
			};
		});/*
	},
	department: function(frm) {
		/*frm.set_value("bsc_indicator", "");
		frm.set_value("indicator_name", "");*/
	},
	uom: function(frm) {
		frm.trigger("change_properties");
	},
	change_properties: function(frm) {
		console.log('in change')
		frm.set_df_property('cumulative_target','req',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('target','read_only',  frm.doc.uom!=='Percent'? 1 : 0);
		frm.set_df_property('jan','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('feb','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('mar','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('apr','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('may','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('jun','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('jul','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('aug','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('sep','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('oct','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('nov','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('dec','read_only',  frm.doc.uom!=='Numerical'? 1 : 0);
		frm.set_df_property('jan_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('feb_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('mar_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('apr_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('may_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('jun_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('jul_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('aug_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('sep_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('oct_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('nov_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('dec_','reqd',  frm.doc.uom=='Percent'? 1 : 0);
		frm.set_df_property('jan__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('feb__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('mar__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('apr__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('may__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('jun__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('jul__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('aug__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('sep__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('oct__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('nov__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);
		frm.set_df_property('dec__','hidden',  frm.doc.uom!=='Cumulative'? 1 : 0);

	},
	validate(frm){
		frm.trigger("calc_target");
	},
	calc_target: function(frm){
		if(frm.doc.uom=='Cumulative'){
				frm.set_value("jan", frm.doc.jan__==1?frm.doc.cumulative_target:0);
				frm.set_value("feb", frm.doc.feb__==1?frm.doc.cumulative_target:0);
				frm.set_value("mar", frm.doc.mar__==1?frm.doc.cumulative_target:0);
				frm.set_value("apr", frm.doc.apr__==1?frm.doc.cumulative_target:0);
				frm.set_value("may", frm.doc.may__==1?frm.doc.cumulative_target:0);
				frm.set_value("jun", frm.doc.jun__==1?frm.doc.cumulative_target:0);
				frm.set_value("jul", frm.doc.jul__==1?frm.doc.cumulative_target:0);
				frm.set_value("aug", frm.doc.aug__==1?frm.doc.cumulative_target:0);
				frm.set_value("sep", frm.doc.sep__==1?frm.doc.cumulative_target:0);
				frm.set_value("oct", frm.doc.oct__==1?frm.doc.cumulative_target:0);
				frm.set_value("nov", frm.doc.nov__==1?frm.doc.cumulative_target:0);
				frm.set_value("dec", frm.doc.dec__==1?frm.doc.cumulative_target:0);
			/*$.each(frm.doc.target_months || [], function(i, d) {
				total +=d.target;
			});*/
			//frm.set_value("target", frm.doc.total);
		}else if(frm.doc.uom=='Numerical'){
			/*$.each(frm.doc.target_months || [], function(i, d) {
				if(d.target!=frm.doc.target && d.target!=0.0 && d.target!=0){
					msgprint(__("Target in {0} must to be equal Target Total",[d.month]));
					frappe.validated = false;
					return false;
				}
			});*/

		}
		else if(frm.doc.uom=='Percent'){
			console.log(frm.doc.jan_+frm.doc.feb_+frm.doc.mar_+frm.doc.apr_+frm.doc.may_+frm.doc.jun_+
				frm.doc.jul_+frm.doc.aug_+frm.doc.sep_+frm.doc.oct_+frm.doc.nov_+frm.doc.dec_)
			if(frm.doc.jan_+frm.doc.feb_+frm.doc.mar_+frm.doc.apr_+frm.doc.may_+frm.doc.jun_+
				frm.doc.jul_+frm.doc.aug_+frm.doc.sep_+frm.doc.oct_+frm.doc.nov_+frm.doc.dec_!==100){
				        msgprint('Total of Percents of Months must to be 100%');
            				validated = false;
					return;
			}
			frm.set_value("jan", frm.doc.target*frm.doc.jan_/100);
			frm.set_value("feb", frm.doc.target*frm.doc.feb_/100);
			frm.set_value("mar", frm.doc.target*frm.doc.mar_/100);
			frm.set_value("apr", frm.doc.target*frm.doc.apr_/100);
			frm.set_value("may", frm.doc.target*frm.doc.may_/100);
			frm.set_value("jun", frm.doc.target*frm.doc.jun_/100);
			frm.set_value("jul", frm.doc.target*frm.doc.jul_/100);
			frm.set_value("aug", frm.doc.target*frm.doc.aug_/100);
			frm.set_value("sep", frm.doc.target*frm.doc.sep_/100);
			frm.set_value("oct", frm.doc.target*frm.doc.oct_/100);
			frm.set_value("nov", frm.doc.target*frm.doc.nov_/100);
			frm.set_value("dec", frm.doc.target*frm.doc.dec_/100);
			/*$.each(frm.doc.target_months || [], function(i, d) {
				total +=d.target;
			});
			if(total!=100){
				msgprint(__("Total of Months Target must to be 100%"));
				frappe.validated = false;
				return false;
			}*/
		}
		frm.set_value("target", frm.doc.jan+frm.doc.feb+frm.doc.mar+frm.doc.apr+frm.doc.may+frm.doc.jun+
			frm.doc.jul+frm.doc.aug+frm.doc.sep+frm.doc.oct+frm.doc.nov+frm.doc.dec);

	}
});
