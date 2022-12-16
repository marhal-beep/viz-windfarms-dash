// Function that filters data
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        filter_function: function (nc, data_wt, data_wf, value_lc, value_ctr, value_cont, value_turb_slider, value_lf, value_dist_slider, value_elev_slider, value_shape) {

            // Create json data for farms and turbines 
            // turbines 
            const keys = Object.keys(data_wt)
            var data_wt_json = [];
            for (let row = 0; row < 359947; row++) {
                templist = []
                for (const key of keys) {
                    templist[key] = data_wt[key][row];
                }
                data_wt_json.push(templist)
            }
            // farms 
            const keys_wf = Object.keys(data_wf)
            var data_wf_json = [];
            for (let row = 0; row < 359947; row++) {
                templist = {};
                for (const key_wf of keys_wf) {
                    templist[key_wf] = data_wf[key_wf][row];

                }
                data_wf_json.push(templist)
            }
            var id_array = [];

            // Filter turbines 
            var filtered_data = data_wt_json.filter(d => value_ctr.includes(d["Country"]) && value_lc.includes(d["Land Cover"]) && value_cont.includes(d["Continent"]) &&
                value_lf.includes(d["Landform"]) && value_shape.includes(d["Shape"]) && (value_turb_slider[0] <= d["Number of turbines"]) &&
                (value_turb_slider[1] >= d["Number of turbines"]) && (value_dist_slider[0] <= d["Turbine Spacing"]) &&
                (value_dist_slider[1] >= d["Turbine Spacing"]) && (value_elev_slider[0] <= d["Elevation"]) &&
                (value_elev_slider[1] >= d["Elevation"]));
            filtered_data.forEach((arr) => { id_array.push(arr.id) });
            var wt_data = [{
                'id': id_array,
            }]


            var wfid_array_2 = [];

            // filter wind farms 
            var filtered_data_2 = data_wf_json.filter(d => (d["WFid"] != -1) && value_ctr.includes(d["Country"]) && value_lc.includes(d["Land Cover"]) && value_cont.includes(d["Continent"]) &&
                value_lf.includes(d["Landform"]) && value_shape.includes(d["Shape"]) && (value_turb_slider[0] <= d["Number of turbines"]) &&
                (value_turb_slider[1] >= d["Number of turbines"]) && (value_dist_slider[0] <= d["Turbine Spacing"]) &&
                (value_dist_slider[1] >= d["Turbine Spacing"]) && (value_elev_slider[0] <= d["Elevation"]) &&
                (value_elev_slider[1] >= d["Elevation"]));
            filtered_data_2.forEach((arr) => { wfid_array_2.push(arr.WFid) })
            var wf_data = [{
                'WFid': wfid_array_2,
            }]

            // only return indexes as json, return number of resulting filtered values for each 
            return [JSON.stringify(wt_data[0]), JSON.stringify(wf_data[0]), filtered_data_2.length.toLocaleString('en').replace(",", "."), filtered_data.length.toLocaleString('en').replace(",", "."),];
        }
    }
}
);







