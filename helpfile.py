import random
from random import sample

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table, html
from plotly.subplots import make_subplots


import turf

pd.options.mode.chained_assignment = None  # default='warn'


# Function that calculates the zoom and center of wind farm to show as scattermapbox plot
# Source: https://stackoverflow.com/questions/63787612/plotly-automatic-zooming-for-mapbox-maps (last access: 24-11-2022)
def zoom_center(bbox, width_to_height: float = 2.0):

    # Get bounding box limits
    maxlon, minlon = bbox[2], bbox[0]
    maxlat, minlat = bbox[3], bbox[1]
    
    # Calculate center
    center = {
        'lon': round((maxlon + minlon) / 2, 6),
        'lat': round((maxlat + minlat) / 2, 6)
    }

    # longitudinal degreee range by zoom level (20 to 1)
    lon_zoom_range = np.array([
        0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
        0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
        47.5136, 98.304, 190.0544, 360.0
    ])

    # calculate zoom with margin to outer points 
    margin = 4
    height = (maxlat - minlat) * margin * width_to_height 
    width = (maxlon - minlon) * margin 
    lon_zoom = np.interp(width, lon_zoom_range, range(20, 0, -1))
    lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
    zoom = round(min(lon_zoom, lat_zoom), 2)

    return zoom, center

# Function tht creats plot of single wind farm with specific visual encoding
# Inputs: wind turbines data that must contain columns [WFid, lon, lat] & WFid 
def plot_single_windfarm_mapbox(clustered_data, wfid):

    # Don't plot standalone turbines
    if (wfid == -1):
        return html.Div('Single turbines cannot be plotted!')

    # Get selected wind farm and transform to class turf points 
    current_wf = clustered_data[clustered_data["WFid"] == wfid]
    wf_geopoints = turf.points(current_wf[["lon", "lat"]].values.tolist())
    
    # Create grid to put on wind farm and store in list
    bbox = turf.bbox(wf_geopoints)
    bbox_buff = [bbox[0] - 0.01, bbox[1]-0.01, bbox[2]+0.01, bbox[3]+0.01]

    # Retrieve central loaction and zoom level of scattermapbox plot in dictionary to add to plot layout 
    zoom, center = zoom_center(bbox_buff)

    # Compute bounding box of plot
    layer=turf.square_grid(bbox_buff,1000, {"units": 'meters'})

    # Retrieve all turbines in bounding box of +- 1° longitudinale/latitudinal
    ll = np.array([(center["lat"]-1), (center["lon"]-1)])  # lower-left
    ur = np.array([(center["lat"]+1), (center["lon"]+1)])  # upper-right
    inidx = np.all(np.logical_and(ll <= clustered_data[["lat", "lon"]], clustered_data[["lat", "lon"]] <= ur), axis=1)
    data_in_box = clustered_data[inidx]

    # color for turbines contained in farm: red
    # for remaining turbines in bounding box: orange 
    data_in_box.loc[data_in_box["WFid"] != wfid, "Color"] = "#FFC000"
    data_in_box.loc[data_in_box["WFid"] == wfid, "Color"] = "#FF0000"
    
    # Create scattermapbox plot 
    fig = go.Figure(go.Scattermapbox(
        lon=list(data_in_box["lon"]),
        lat=list(data_in_box["lat"]), 
        mode='markers', 
        name = "", 
        marker=dict(color=data_in_box["Color"]), 
        hovertemplate = [f'Windfarm ID: {string1}<br>Turbine Spacing (m): {string2}<br>Number of turbines: {string3}<br>Elevation (m): {string4}<br>Land Cover: {string5}<br>Landform: {string6}<br>Country: {string7}<br>Continent: {string8}<br>Shape: {string9}'
                    for string1, string2, string3, string4, string5, string6, string7, string8, string9 in zip(data_in_box["WFid"], data_in_box["Turbine Spacing"], data_in_box["Number of turbines"], data_in_box["Elevation"], data_in_box["Land Cover"], data_in_box["Landform"], data_in_box["Country"],data_in_box["Continent"],  data_in_box["Shape"])]
        ))

    # Update background layer 
    fig.update_mapboxes(
                style= "mapbox://styles/zwiefele/cl4dap44m001d15pfttaws59k", 
                accesstoken="pk.eyJ1IjoiendpZWZlbGUiLCJhIjoiY2wxeTAzazJxMDcwaTNibXQ5aTRyMno0bSJ9.zPSVI0wOb_sIXGH-tgHNVw"
                )

    fig.update_layout(
        mapbox=dict(layers=[dict(sourcetype ='geojson',source =layer,type = 'line', color = '#454545',opacity = 0.2,line=dict(width=1))]), 
        margin=dict(l=0, r=0, t = 0, b=0),
        hoverlabel=dict(
            bgcolor="#AEDCC8",
            font_size=11,
            font_family='Montserrat, sans-serif'
        )
    )
    fig.layout.mapbox.center = center
    fig.layout.mapbox.zoom = zoom



    return fig


# Creates frequency view: frequency distribution of wind farms and turbines oover selected variable and table showing summary statistics
# Inputs are full wind tubrines and wind farm data, and variable over which to show distribution as String
def plot_wf_histograms(filtered_wt_data, filtered_wf_data, y_axis = "Country"):

    # Distinguish between stand-alone and non stand-alone turbines and name them accordingly  
    filtered_wt_data['grouping'] = 'contained in wind farm'
    filtered_wt_data.loc[(filtered_wt_data["WFid"] == -1), 'grouping'] = 'single turbine'

    # Create bar chart for categorical varible on y-axis
    if y_axis in ["Country", "Continent", "Land Cover", "Landform", "Shape" ]:
        y_axis_label = y_axis

        # wind farms bar chart
        xaxis_groupby = filtered_wf_data[y_axis].value_counts()
        category_order_names = xaxis_groupby.keys().tolist()
        xaxis_groupby = xaxis_groupby.reset_index().sort_values(y_axis)

        fig1_histwf = px.histogram(xaxis_groupby,x=y_axis,y ="index", color_discrete_sequence=['#F46281'], 
                        category_orders={y_axis: category_order_names}, labels={"index": "Count of Wind farms", y_axis: y_axis})

        # Summary statistics of wind farm sizes in categories of variable
        wfsizedistr_datatable =filtered_wf_data.groupby(y_axis)["Number of turbines"].describe().round(2).loc[category_order_names].reset_index()
        fig2_hist_wfsize = [dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in wfsizedistr_datatable.columns],
            data=wfsizedistr_datatable.to_dict('records'), 
            style_as_list_view=True,
            fixed_rows={'headers': True},
            style_cell={'textAlign': 'center', 
                'fontSize':9, 
                'font-family':'Verdana, sans-serif'
                },
            style_table={"padding-left":"10px","padding-right":"10px", "background-color":"#F9F9F9", "color":"#2C3333"},
            style_header={
                'backgroundColor': '#2C3333',
                'color': 'white'
                },
            style_data={
                'height': 'auto',
                'minWidth': '8px', 
                # 'width': 'auto', 
                'maxWidth': '15px',     
                'whiteSpace': 'pre-line',
                "background-color":"#F4F4F4",
                },
            sort_action="native")]
        categories_fig3 = np.unique(filtered_wt_data[y_axis])
        not_contained = [i for i in categories_fig3 if i not in category_order_names]
        for x in not_contained:
            category_order_names.append(x)

        # wind turbines chart, color according to stand-alone or not 
        fig3_histwt =  px.histogram(filtered_wt_data, y = y_axis, color="grouping",color_discrete_sequence=["#F46281", "#f4a261"], 
                        category_orders={ y_axis: category_order_names,"grouping":['in wind farm','single turbine']})


    # Create histogram for categorical varible on y-axis
    else:
        # Histogram of wind farms 
        if y_axis in ["Elevation", "Turbine Spacing"]:
            y_axis_label = y_axis + " (m)"
        else: y_axis_label = y_axis
        fig1_histwf = px.histogram(filtered_wf_data,y =y_axis,opacity=0.8, color_discrete_sequence=['#F46281'], nbins = 200,  
            text_auto='.2s', labels={
                        "index": "Count of Wind farms",
                        y_axis: y_axis_label,
                    })

        # Summary statistics about varible itself
        turbingesdist_datatable =filtered_wf_data[y_axis].describe().round(2).reset_index()
        fig2_hist_wfsize = [dash_table.DataTable(
            # id='table-container',
            columns=[{"name": i, "id": i} for i in turbingesdist_datatable.columns],
            data=turbingesdist_datatable.to_dict('records'), 
            style_as_list_view=True,
            fixed_rows={'headers': True},
            style_cell={'textAlign': 'center', 
                'fontSize':9, 
                'font-family':'Verdana, sans-serif', 
                },
            style_table={"padding-left":"10px","padding-right":"10px", "background-color":"#F4F4F4", "color":"#2C3333"},
            style_header={
                'backgroundColor': '#2C3333',
                'color': 'white'
            },
            style_data={
                'height': 'auto',
                'minWidth': '8px', 
                # 'width': 'auto', 
                'maxWidth': '15px',     
                'whiteSpace': 'pre-line',
                "background-color":"#F4F4F4",
            },
            sort_action="native")]

        # Histogram of turbines, color according to stand-alone or not 
        fig3_histwt =  px.histogram(filtered_wt_data, y = y_axis,  opacity=0.8, color="grouping",color_discrete_sequence=["#F46281", "#f4a261"], 
                        category_orders={ "grouping":['turbines in wind farms','single turbines']}, nbins=200)

    # Update layouts of histograms 
    fig1_histwf.update_layout(
        xaxis_title="Wind Farms count",
        yaxis_title=y_axis_label, 
        margin = {'r':0,'t':40,'l':0,'b':0}, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='#F4F4F4', 
        font_family='Montserrat, sans-serif',
        font_color="#2C3333",
        title_font_family='Montserrat, sans-serif',
        title_font_color="#2C3333",
        legend_title_font_color="#2C3333",
        hovermode ="y unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            font_family="Montserrat, sans-serif"
        ),
        )
    fig1_histwf.update_traces(hovertemplate='Number of wind farms: %{x}') #

    fig3_histwt.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            font_family="Montserrat, sans-serif"
        ),
        xaxis_title="Wind Turbines count",
        yaxis_title=y_axis_label,
        legend_title=None,
        margin = {'r':15,'t':30,'l':15,'b':15}, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='#F4F4F4', 
        font_family='Montserrat, sans-serif',
        font_color="#2C3333",
        title_font_family='Montserrat, sans-serif',
        title_font_color="#2C3333",
        hovermode ="y unified"

    )
    fig3_histwt.update_traces(hovertemplate='%{x}') #



    return fig1_histwf, fig2_hist_wfsize, fig3_histwt


# Creates Random Wind farms view: PLots poster-like image of multiple wind farms with specific visual encodings
# Inputs are: 
# wind turbines dataset that contains all features 
# wind farms dataset that contains [WFid, lon, lat]
# Random seed for drawing sample
# Variable after which the wind farms are sorted
# number of rows and columns of raster poster
def plot_wf_poster(clustered_data, filtered_wf_data, seed = 0, sorting_condition="Number of turbines",  plot_rows=5, plot_col = 5):

    # Draw a random sample of wind farms (from wf data index) that match the filtered data
    wfids = filtered_wf_data.WFid.to_list()
    random.seed(seed) # set seed for reproducibility in drawing sample 
    random_wfsids = sample(wfids,plot_rows*plot_col)
    random_wfs_ids = filtered_wf_data[filtered_wf_data["WFid"].isin(random_wfsids)].sort_values(sorting_condition)["WFid"].to_list()

    # Initialize mapbox figure for each subplot 
    specs = [{"type": 'mapbox'}]
    i = 1
    while (i  < (plot_col)):
        specs.append( {"type": 'mapbox'})
        i = i+1
    j = 0
    specs_list = []
    while (j < (plot_rows)):
        specs_list.append(specs)
        j = j+1

    # Create subplot figure and set common map layer
    fig = make_subplots(rows=plot_rows, cols=plot_col, horizontal_spacing = 0.01,vertical_spacing = 0.02,
         specs= specs_list)
    fig.update_mapboxes(
                style= "mapbox://styles/zwiefele/cl4dap44m001d15pfttaws59k", 
                accesstoken="pk.eyJ1IjoiendpZWZlbGUiLCJhIjoiY2wxeTAzazJxMDcwaTNibXQ5aTRyMno0bSJ9.zPSVI0wOb_sIXGH-tgHNVw",
                )
    fig.update_layout(
        title = "Random Wind Farms" ,
        showlegend=False, 
        )

    x = 0

    # Initialize lists where levels for center and zoom, and overlaying grids will be stored
    zooms = []
    centers = []
    grids = []

    # Loop over each wind farm and fill row and columns wise 
    for i in range(1, plot_rows + 1):
        for j in range(1, plot_col + 1):
            #update common attributes:

            # Get wind farms through random ids sample
            current_wfid = random_wfs_ids[x]
            current_wf = clustered_data[clustered_data["WFid"] == current_wfid]
            wf_geopoints = turf.points(current_wf[["lon", "lat"]].values.tolist())

            # Create grid to put on wind farm and store in list
            bbox = turf.bbox(wf_geopoints)
            bbox_buff = [bbox[0] - 0.01, bbox[1]-0.01, bbox[2]+0.01, bbox[3]+0.01] # add margin
            layer=turf.square_grid(bbox_buff,1000, {"units": 'meters'} )
            grids.append(layer) 

            # Retrieve central loaction and zoom level of scattermapbox plot and add to list
            zoom, center = zoom_center(bbox_buff)
            centers.append(center)
            zooms.append(zoom)

            # Retrieve all turbines in bounding box of +- 1° longitudinale/latitudinal
            ll = np.array([(center["lat"]-1), (center["lon"]-1)])  # lower-left
            ur = np.array([(center["lat"]+1), (center["lon"]+1)])  # upper-right
            inidx = np.all(np.logical_and(ll <= clustered_data[["lat", "lon"]], clustered_data[["lat", "lon"]] <= ur), axis=1)
            data_in_box = clustered_data[inidx]
            data_in_box["group"] = 0

            # color for turbines contained in farm: red
            # for remaining turbines in bounding box: orange 
            data_in_box.loc[data_in_box["WFid"].isin([current_wfid]),"group"] = "#FF0000"
            data_in_box.loc[~data_in_box["WFid"].isin([current_wfid]),"group"] = "#FFC000"
            
            # Create plot of single wind farm and add as trace to subplot figure
            fig.add_trace(go.Scattermapbox(
                lon=list(data_in_box["lon"]),
                lat=list(data_in_box["lat"]), 
                mode='markers', 
                name='',
                marker=dict(color=data_in_box["group"]), 
                text = ["test"],
                hovertemplate = [f'Windfarm ID: {string1}<br>Turbine Spacing (m): {string2}<br>Number of turbines: {string3}<br>Elevation (m): {string4}<br>Land Cover: {string5}<br>Landform: {string6}<br>Country: {string7}<br>Continent: {string8}<br>Shape: {string9}'
                    for string1, string2, string3, string4, string5, string6, string7, string8, string9 in zip(data_in_box["WFid"], data_in_box["Turbine Spacing"], data_in_box["Number of turbines"], data_in_box["Elevation"], data_in_box["Land Cover"], data_in_box["Landform"], data_in_box["Country"],data_in_box["Continent"],  data_in_box["Shape"])]
            ), row=i, col=j)

            x=x+1


    # Adjust figure layout 
    temp= min(plot_rows, plot_col)
    fig.update_layout(
        height = 300+temp*150, 
        width = 400+temp*150, 
        autosize = True, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='#F4F4F4', 
        margin = {'r':0,'t':0,'l':0,'b':0}, 
        hoverlabel=dict(
            bgcolor="#AEDCC8",
            font_size=11,
            font_family='Montserrat, sans-serif'
        )
    )
    # Update grid layers of figures 
    for m, g in zip(fig.data, grids):
        exec("fig.update_layout("+ str(m.subplot) 
        + "=dict(layers=[dict(sourcetype = 'geojson',source ="
        +str(g) + ",type = 'line', color = '#454545',opacity = 0.2,line=dict(width=1))]))")
                
    # Update centers of figures 
    for m, c in zip(fig.data, centers):
        exec("fig.layout." + m.subplot+"[\"center\"] = " + str(c))
    # Update centers of figures 
    for m, z in zip(fig.data, zooms):
        exec("fig.layout." + m.subplot+"[\"zoom\"] = " + str(z))

    return fig