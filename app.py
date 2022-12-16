# General
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq

# For Map Visualization
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, Input, Output, State, callback_context, ctx, dcc
from dash.dependencies import ClientsideFunction, Input, Output
from dash_extensions.javascript import assign

# From files 
from helpfile import *

# Read data
data_windfarms = pd.read_csv("data/wf_data_final.csv")#.iloc[1:5000]
data_windturbines = pd.read_csv("data/wt_data_final.csv")

# Create dropdown menu contents
landcover_options = [{'label': i, 'value': i} for i in sorted(data_windfarms["Land Cover"].unique())]
country_options = [{'label': i, 'value': i} for i in sorted(data_windturbines["Country"].unique())]
continent_options = [{'label': i, 'value': i} for i in sorted(data_windturbines["Continent"].unique())]
landform_options = [{'label': i, 'value': i} for i in sorted(data_windturbines["Landform"].unique())]
shape_options = [{'label': i, 'value': i} for i in data_windfarms["Shape"].dropna().unique()]
column_names = ['Country', 'Continent', 'Land Cover','Landform','Shape', 'Number of turbines','Elevation' ,'Turbine Spacing'   ]
x_axis_options = [{'label': i, 'value': i} for i in column_names]

# Set defaults for menus
landcover_defaults = [o["value"] for o in landcover_options]
country_defaults = [o["value"] for o in country_options]
continent_defaults = [o["value"] for o in continent_options]
landform_defaults = [o["value"] for o in landform_options]
shape_defaults = [o["value"] for o in shape_options]
x_axis_options_default = [o["value"] for o in x_axis_options]

# Map layers for leaflet in Map View 
mapbox_url = "https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{{z}}/{{x}}/{{y}}{{r}}?access_token={access_token}"
mapbox_token ="pk.eyJ1IjoiendpZWZlbGUiLCJhIjoiY2wxeTAzazJxMDcwaTNibXQ5aTRyMno0bSJ9.zPSVI0wOb_sIXGH-tgHNVw"  # settings.MAPBOX_TOKEN
mapbox_ids = ["light-v9", "dark-v9", "streets-v9", "outdoors-v9", "satellite-streets-v9"]


# Styles for tabs 
tabs_styles = {
    'height': '35px', 
    'display':'flex', 
    'marginLeft':'5px',
    'marginRight':'5pxs',
    "width":"99%",
    "textAlign":"center"

}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '5px',
    'fontWeight': 'bold',
    'backgroundColor':'#fcfcfc',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#65BB95',
    'color': "#FFFFFF",
    'padding': '6px'
}

# Create data overlays windfarms/windturbines for Map View 
point_to_layer = assign("function(feature, latlng, context) {mmarker = L.circleMarker(latlng, {radius:5, fillOpacity: 0.5}).bindPopup(\"Displayed\"); return mmarker.openPopup() ;}")
# geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=point_to_layer))
cluster_wf = dl.GeoJSON( id="geojson", options=dict(pointToLayer=point_to_layer),  format = "geobuf",cluster=True, zoomToBoundsOnClick=True, superClusterOptions={"radius": 100, "maxZoom":11})#,children=[dl.Popup("Displayed Windfarm")]
cluster_wt = dl.GeoJSON(id="geojson_wt", options=dict(pointToLayer=point_to_layer),   format = "geobuf", cluster=True, zoomToBoundsOnClick=True, superClusterOptions={"radius": 100, "maxZoom":11})#,children=[dl.Popup("Displayed Windfarm")]
#format="geobuf",

# Initiate app
app = Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])
server = app.server

### LAYOUT
app.layout = html.Div([
    
    html.Div(children=[
        # Title
        html.H2("Visualizing Wind Farms", className = "title"), 

        # Information text on number of displayed turbines     
        dbc.Card(                                            
                dbc.CardBody(
                    [
                        html.H4(children=[], className="card-title", id = "filter_application"),    
                        html.P("of 20.607 Wind Farms", className="card-text"),
                    ]
                ),
            ),

        # Information text on number of displayed turbines   
        dbc.Card(     
            dbc.CardBody(
                [
                    html.H4(children=[], className="card-title", id = "filter_application_wts"),
                    html.P("of 359.947 Wind Turbines", className="card-text"),
                ]
            ),
        ),
        
        # Error Showing Button with popover
        html.Button( 
            "!",
            id="popover-alt-target",
            className="popover-alt-target-1",
        ),
        dbc.Popover( #
            id = "popover_content", 
            body=True,
            target="popover-alt-target",
            trigger="hover",
            class_name="popover"
        ),

        # Apply Filter button 
        html.Button(id='submit-button-state', n_clicks=0, children='Apply Filter', className="filterButton"),# Apply filter button
        daq.ToggleSwitch(
            id='my-toggle-switch',
            value=False,  
            label='Show Filter',
            className = "toggleSwitch",
            size = 40, 
            color = "#68c49b",
        ), 

        # Show Questions button 
        daq.ToggleSwitch(
            id='my-toggle-switch-questionnaire',
            value=False,  
            label='Questions',
            className = "toggleSwitch",
            size = 20, 
            color = "#68c49b")

        ], className = "headerClass"
        
    ), 
                
    # Filter Options
    html.Div(children  =[ 

        # Categorical dropdowns
        html.Div(children = [
                dbc.Container(
                        children=[
                            html.H6('Country'),
                            html.Details([
                            html.Summary('Select country...', className="app-summaries"),
                            html.Br(),
                            dbc.Col([
                                dcc.Checklist(["All"],["All"], id="dd_all_countries", inline=True, className = "checkboxes_label_all"),
                                dcc.Checklist(
                                    id="dd_country",
                                    options=country_options,
                                    value=country_defaults,
                                    inline = False,
                                    labelStyle = { 'marginLeft':'7px','display':'block'},
                                    className = "checkboxes_label"
                                    )               
                                
                                ])
                            ])
                    ], className="filterBoxes"),

                dbc.Container(
                        children=[
                            html.H6('Continent'),
                            html.Details([
                            html.Summary('Select continent...', className="app-summaries"),
                            html.Br(),
                            dbc.Col([
                                dcc.Checklist(["All"],["All"], id="dd_all_continent", inline=True, className = "checkboxes_label_all"),
                                dcc.Checklist(
                                    id="dd_continent",
                                    options=continent_options,
                                    value=continent_defaults,
                                    inline = False,
                                    labelStyle = { 'marginLeft':'7px','display':'block'},
                                    className = "checkboxes_label"
                                    )])])
                    ], className="filterBoxes"),

                dbc.Container(
                        children=[
                            html.H6('Land Cover'),
                            html.Details([
                            html.Summary('Select land cover...', className="app-summaries"),
                            html.Br(),
                            dbc.Col([
                                dcc.Checklist(["All"],["All"], id="dd_all_landcover", inline=True, className = "checkboxes_label_all"),
                                dcc.Checklist(
                                    id="dd_landcover",
                                    options=landcover_options,
                                    value=landcover_defaults,
                                    inline = False,
                                    labelStyle = { 'marginLeft':'7px','display':'block'},
                                    className = "checkboxes_label")])])], className="filterBoxes"),

                    dbc.Container(
                        children=[
                            html.H6('Land Form'),
                            html.Details([
                            html.Summary('Select land form...', className="app-summaries"),
                            html.Br(),
                            dbc.Col([
                                dcc.Checklist(["All"],["All"], id="dd_all_landform", inline=True, className = "checkboxes_label_all"),
                                dcc.Checklist(
                                    id="dd_landform",
                                    options=landform_options,
                                    value=landform_defaults,
                                    inline = False,
                                    labelStyle = { 'marginLeft':'7px','display':'block'},
                                    className = "checkboxes_label"
                                    )])])], className="filterBoxes"),

                    dbc.Container(
                                    children=[
                                        html.H6('Shape'),
                                        html.Details([
                                        html.Summary('Select shape', className="app-summaries"),
                                        html.Br(),
                                        dbc.Col([
                                            dcc.Checklist(["All"],["All"], id="dd_all_shape", inline=True, className = "checkboxes_label_all"),
                                            dcc.Checklist(
                                                id="dd_shape",
                                                options=shape_options,
                                                value=shape_defaults,
                                                labelStyle = { 'marginLeft':'7px','display':'block'},
                                                className = "checkboxes_label"
                                                )               
                                            
                                            ]
                                            )
                                        ])
                                ], className="filterBoxes"), 
                ], className = "allFilterBoxesToprow"), 

            # Numerical sliders
            html.Div(children=[

                html.Div(children=[
                    html.H6('Number of Turbines'),
                    dcc.RangeSlider(1, 3296, 1, value=[1, 4086],marks=None, id='sd_turbines', tooltip={"placement": "bottom", "always_visible": True})
                ],  className = "sliderBox"),


                html.Div(children=[
                    html.H6('Elevation Level (m)'),
                    dcc.RangeSlider(-46, 4684, 1, value=[-46, 4684],marks=None, id='sd_elevation', tooltip={"placement": "bottom", "always_visible": True})
                ],  className ="sliderBox"),

                html.Div(children=[
                    html.H6('Turbine Spacing (m)'),
                    dcc.RangeSlider(10, 13155, 10, value=[10, 13155],marks=None, id='sd_distance', tooltip={"placement": "bottom", "always_visible": True})
                ], className="sliderBox"),

            ], className="sliders_class"), 
        ],  className = "allFilters", id = "allfilters"),

        # Evaluation Questions
        html.Div(
            dcc.Tabs([
                dcc.Tab(label='EXQ1', children=[
                    html.Div(children =["Which land form is predominant for the installation of windfarms in Austria?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),

                dcc.Tab(label='EXQ2', children=[
                    html.Div(children =["Where do you find the biggest wind farms in the world? How is their turbine spacing distributed?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),

                dcc.Tab(label='Q1', children=[
                    html.Div(children =["Which land cover is predominant for the installation of Wind Farms on a global scale?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),


                dcc.Tab(label='Q2', children=[
                    html.Div(children =["How do wind farms in the USA, Germany and China compare in terms of number of wind farms and wind farm size?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),

                dcc.Tab(label='Q3', children=[
                    html.Div(children =["Where are the highest wind farms in the world located?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),

                dcc.Tab(label='Q4', children=[
                    html.Div(children =["How does the turbine spacing of wind farms in Oceans and seas compare to wind farms on Agricultural land cover?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),

                dcc.Tab(label='Q5', children=[
                    html.Div(children =["Filter the data for wind farms with more than 10 turbines and look at 3x3 random wind farms. Set the seed to 0. Which wind farm has the smallest spacing between the turbines?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),

                dcc.Tab(label='Q6', children=[
                    html.Div(children =["(Refers to Q5) Which wind farms (if any) are positioned on a summit or ridge?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),


                dcc.Tab(label='Q7', children=[
                    html.Div(children =["Is there a question you would like to answer with the tool?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),
                
                dcc.Tab(label='FQ1', children=[
                    html.Div(children =["Have you learned any new insights about the wind industry? If so, which ones?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),

                dcc.Tab(label='FQ2', children=[
                    html.Div(children =["Did the visualization confirm any assumptions you had about the wind industry before?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),

                dcc.Tab(label='FQ3VA', children=[
                    html.Div(children =["Can you give general feedback on the visualization in terms of user interface, functionalities, etc.?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),

                dcc.Tab(label='FQ3DE', children=[
                    html.Div(children =["If the visualization data was updated regularly, would the tool be useful to you in your work?"], className = "questions")
                    ], style=tab_style, selected_style=tab_selected_style),
                
            ], className=  "tabqt"),
        id  = "QuestionnairTabs"),


    # Tabs for the three views    
    dcc.Tabs([
        
        # Tab 1 content: Map View  
        dcc.Tab(label='Map', children=[
            html.Div(children = [
                
            dbc.Spinner(children=[
                dbc.Container(children = [
                    dbc.Label("World Map", style = {'marginLeft':'5px'}),
                    html.Div(dl.Map([#dl.TileLayer(),        
                                dl.LayersControl(collapsed=False,
                                    children=[dl.BaseLayer(dl.LayerGroup(cluster_wf), name="Wind Farms", checked=True), 
                                    dl.BaseLayer(dl.LayerGroup(cluster_wt), name="Wind Turbines", checked=False)], id = "MapLeafletLayersControl"), 
                                dl.LayersControl(
                                    [dl.BaseLayer(dl.TileLayer(url=mapbox_url.format(id="light-v9", access_token=mapbox_token, noWrap= True)),
                                                name="Light", checked=True),
                                    dl.BaseLayer(dl.TileLayer(url=mapbox_url.format(id="satellite-streets-v9", access_token=mapbox_token, noWrap= True)),
                                                name="Satellite", checked=False), 
                                    dl.BaseLayer(dl.TileLayer(url=mapbox_url.format(id="dark-v9", access_token=mapbox_token, noWrap= True)),
                                                name="Dark", checked=False), 
                                    dl.BaseLayer(dl.TileLayer(url=mapbox_url.format(id="outdoors-v9", access_token=mapbox_token, noWrap= True)),
                                                name="Outdoor", checked=False)
                                                ]), 
                                dl.GestureHandling(), 
                                dl.MeasureControl(position="topleft", primaryLengthUnit="meters", primaryAreaUnit="hectares",
                                                        activeColor="#214097", completedColor="#972158"),
                                dl.ScaleControl(position="bottomleft")
                                

                            ], 
                    center=(33.256890, -3.810381), 
                    zoom=2, 
                    preferCanvas=True,
                    ),className = "MapBoxLeaflet")], style = {'display':'inline-grid'}), 
                ], size="lg", color="secondary", type="border", fullscreen=False, spinnerClassName = "loadingSpinner"),

            dbc.Container(children = [
                dbc.Label("Single Wind Farm", style ={'marginLeft':'-3%'}),
                html.Div(children = ["   Click on a marker to plot the related wind farm."], id = "singleWF",  className = "MapBox")], style = {"display":"inline-grid"})], className = "tab1")

        ], style=tab_style, selected_style=tab_selected_style),


        # Tab 2 content: Frequency View 
        dcc.Tab(label='Frequency Distribution', children=[
            
            html.Div(children=[
                html.H6('y-Axis'),
                dcc.Dropdown(id="dd_xaxis", value=x_axis_options_default[1], options=x_axis_options, className = "checkboxes_label_all")
            ], style = {"display": "block", "width":"25%", "marginLeft":"15px"}), 
            
            dbc.Spinner(children=[

                html.Div(children = 
                    [
                    
                    dbc.Container(children = [
                        dbc.Label("Wind Turbines"),
                        html.Div(children=[dcc.Graph(id = "hist_wtcount_graph")])
                        ], className = "histComponent"),
                    dbc.Container(children = [
                        dbc.Label("Wind Farms"),
                        html.Div(children=[dcc.Graph(id = "hist_wfcount_graph")])
                        ], className = "histComponent"),
                    
                    dbc.Container(children = [
                        dbc.Label("Wind Farm Descriptive Summary Statistics"),
                        html.Div(id  = "hist_turbinescountgrouped_graph", children=[], style = {'height':'80vh'})
                        ], className = "histComponent")    
                    ],
                style={'height': "100%", 'width': "100%", 'display':'flex' }

                )
            ], size="lg", color="secondary", type="border", fullscreen=False, spinnerClassName = "loadingSpinner"),
        ], style=tab_style, selected_style=tab_selected_style),


        # Tab 3 content: Random wind farms view
        dcc.Tab(label='Show me some Wind Farms!', children=[
            html.Div(children = [

                html.Div(children=[
                    html.H6('Sorting Feature'),
                    dcc.Dropdown(id="dd_sort", value="Continent", options=x_axis_options)
                    ], className = "posterFilterElement"),


                html.Div(children=[             
                    html.H6('Seed'),
                    dcc.Input(id='ip_seed', type='number', min=0, max=1000000, step=1, value = 0, placeholder="Seed")       
                    ], className = "posterFilterElement2" ),
                
                
                html.Div(children=[             
                    html.H6('Plot Rows'),
                    dcc.Input(id='ip_plotrows', type='number', min=1, max=10, step=1, value = 3, placeholder="Plot Rows")       
                    ], className = "posterFilterElement2"), 

                html.Div(children=[             
                    html.H6('Plot Columns'),
                    dcc.Input(id='ip_plotcols', type='number', min=1, max=10, step=1, value = 3 , placeholder="Plot Columns")       
                    ],  className = "posterFilterElement2"), 

            ], className= "posterFilter"), 
            # html.Div(
            dbc.Container(children = [
                dbc.Label("Random Wind Farms"),
                dbc.Spinner(children=[
                    html.Div(children=[dcc.Graph(id = "poster_graph", style={'height': '90%'})])
                ], size="lg", color="secondary", type="border", fullscreen=False, spinnerClassName = "loadingSpinner"),
            ], className = "posterGraph")
            # ]), className = "posterGraph")
        ], style=tab_style, selected_style=tab_selected_style),
        
    ], style = tabs_styles, id = "tabs"), 
  

    # Clientside stores for data and filtering results
    dcc.Store(data = data_windfarms.to_dict('list'), id='store_all_wf_data', storage_type="memory"), 
    dcc.Store(data =  data_windturbines.to_dict('list'),id='store_all_wt_data', storage_type = "memory"),
    dcc.Store(id='filtered_wt_intermediate', storage_type="memory"), 
    dcc.Store(id='filtered_wf_intermediate', storage_type="memory"),

],className = "allPage")

### CALLBACKS

# Callback to show questionnaire
app.clientside_callback(
    """
    function(value) {
        if(value === true) {
            return {'display': 'block'};
        } else {
            return {'display': 'none'}
        }
    }
    """,
    Output('QuestionnairTabs', 'style'),
    [Input('my-toggle-switch-questionnaire', 'value')]
)

# Callback to show filter interface 
app.clientside_callback(
    """
    function(value) {
        if(value === true) {
            return {'display': 'block'};
        } else {
            return {'display': 'none'}
        }
    }
    """,
    Output('allfilters', 'style'),
    [Input('my-toggle-switch', 'value')]
)

# Filter clientside-callback
app.clientside_callback(
   ClientsideFunction(
        namespace='clientside',
        function_name='filter_function'
    ),
    Output(component_id="filtered_wt_intermediate", component_property="data"),
    Output(component_id="filtered_wf_intermediate", component_property="data"),
    Output( "filter_application", "children"), 
    Output( "filter_application_wts", "children"), 

    Input('submit-button-state', 'n_clicks'),
    State('store_all_wt_data', 'data'), 
    State('store_all_wf_data', 'data'), 
    State(component_id="dd_landcover", component_property="value"),
    State(component_id="dd_country", component_property="value"),
    State(component_id="dd_continent", component_property="value"),
    State(component_id="sd_turbines", component_property="value"),
    State(component_id="dd_landform", component_property="value"), 
    State(component_id="sd_distance", component_property="value"), 
    State(component_id="sd_elevation", component_property="value"), 
    State(component_id="dd_shape", component_property="value")
)

# Checklist synchronisation Country
@app.callback(
    Output("dd_country", "value"),
    Output("dd_all_countries", "value"),
    Input("dd_country", "value"),
    Input("dd_all_countries", "value"),
)
def sync_checklists(selected_filter_var, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dd_country":
        all_selected = ["All"] if set(selected_filter_var) == set(country_defaults) else []
    else:
        selected_filter_var = country_defaults if all_selected else []
    return selected_filter_var, all_selected

# Checklist synchronisation Land Cover
@app.callback(
    Output("dd_landcover", "value"),
    Output("dd_all_landcover", "value"),
    Input("dd_landcover", "value"),
    Input("dd_all_landcover", "value"),
)
def sync_checklists(selected_filter_var, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dd_landcover":
        all_selected = ["All"] if set(selected_filter_var) == set(landcover_defaults) else []
    else:
        selected_filter_var = landcover_defaults if all_selected else []
    return selected_filter_var, all_selected

# Checklist synchronisation Land Form
@app.callback(
    Output("dd_landform", "value"),
    Output("dd_all_landform", "value"),
    Input("dd_landform", "value"),
    Input("dd_all_landform", "value"),
)
def sync_checklists(selected_filter_var, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dd_landform":
        all_selected = ["All"] if set(selected_filter_var) == set(landform_defaults) else []
    else:
        selected_filter_var = landform_defaults if all_selected else []
    return selected_filter_var, all_selected

# Checklist synchronisation Shape
@app.callback(
    Output("dd_shape", "value"),
    Output("dd_all_shape", "value"),
    Input("dd_shape", "value"),
    Input("dd_all_shape", "value"),
)
def sync_checklists(selected_filter_var, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dd_shape":
        all_selected = ["All"] if set(selected_filter_var) == set(shape_defaults) else []
    else:
        selected_filter_var = shape_defaults if all_selected else []
    return selected_filter_var, all_selected

# Checklist synchronisation continent
@app.callback(
    Output("dd_continent", "value"),
    Output("dd_all_continent", "value"),
    Input("dd_continent", "value"),
    Input("dd_all_continent", "value"),
)
def sync_checklists(selected_filter_var, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dd_continent":
        all_selected = ["All"] if set(selected_filter_var) == set(continent_defaults) else []
    else:
        selected_filter_var = continent_defaults if all_selected else []
    return selected_filter_var, all_selected


# Callback to show single WF plot from Tab 1 on click 
@app.callback(
    Output("singleWF", "children"),

    Input("geojson", "click_feature"),
    Input("geojson_wt", "click_feature"),
    prevent_initial_call=True
)
def update_tooltip(feature1, feature2):
    triggered_id = ctx.triggered_id
    if (triggered_id == 'geojson'):
         return draw_wf_graph(feature1)
    # elif triggered_id == 'geojson_wt':
    #      return draw_wf_graph(feature2)
    else: 
        dash.exceptions.PreventUpdate

def draw_wf_graph(feature):
    if feature is not None: 
        if "WFid" in feature["properties"]:
            wfid = int(str(feature['properties']["WFid"]))
            if (wfid == -1):
                return "Turbines that do not belong to a wind farm cannot be plotted!"
            fig = plot_single_windfarm_mapbox(data_windturbines, wfid)
            return dcc.Graph(figure=fig)
        else: 
            return "   Click on a marker to plot the related windfarm."
    else: 
        return "   Click on a marker to plot the related windfarm."



# Map View 
@app.callback(
    Output(component_id="geojson", component_property='data'),
    Output(component_id="geojson_wt", component_property='data'), 
    # Output(component_id="loader_stoer", component_property='data'), 
    Input(component_id="filtered_wt_intermediate", component_property="data"),
    Input(component_id="filtered_wf_intermediate", component_property="data"),    
)

def update_tab1(filtered_wt_data_json, filtered_wf_data_json):
    filtered_wt_data_idx = pd.read_json(filtered_wt_data_json).iloc[:, 0].tolist()
    filtered_wf_data_idx = pd.read_json(filtered_wf_data_json).iloc[:, 0].tolist()
    filtered_wt_data = data_windturbines[data_windturbines.id.isin(filtered_wt_data_idx)][["lon", "lat"]]
    filtered_wf_data = data_windfarms[data_windfarms.WFid.isin(filtered_wf_data_idx)][["lon", "lat", "WFid"]]
    # Tab 1
    # geojson = 
    # geojson_wt = 
    dicts = dlx.geojson_to_geobuf(dlx.dicts_to_geojson(filtered_wf_data.to_dict('records'), lon="lon"))
    dicts_wt = dlx.geojson_to_geobuf(dlx.dicts_to_geojson(filtered_wt_data.to_dict('records'), lon="lon"))
    # print(fil)
    return dicts, dicts_wt#, [""]
    
# Frequency View
@app.callback(

    Output(component_id="hist_wfcount_graph", component_property='figure'),
    Output(component_id="hist_turbinescountgrouped_graph", component_property='children'), 
    Output(component_id="hist_wtcount_graph", component_property='figure'), 

                
    Input(component_id="dd_xaxis", component_property="value"), 
    Input(component_id="filtered_wt_intermediate", component_property="data"),
    Input(component_id="filtered_wf_intermediate", component_property="data"),    

)
def update_tab2( value_xaxis,  filtered_wt_data_json, filtered_wf_data_json,):
    #Read data
    filtered_wt_data_idx = pd.read_json(filtered_wt_data_json).iloc[:, 0].tolist()
    filtered_wf_data_idx = pd.read_json(filtered_wf_data_json).iloc[:, 0].tolist()
    filtered_wt_data = data_windturbines[data_windturbines.id.isin(filtered_wt_data_idx)]
    filtered_wf_data = data_windfarms[data_windfarms.WFid.isin(filtered_wf_data_idx)]

    histogram_plots  = plot_wf_histograms(filtered_wt_data, filtered_wf_data, x_axis = value_xaxis )

    return histogram_plots[0], histogram_plots[1], histogram_plots[2]#, poster_figure


# Random Wind Farms View 
@app.callback(
    Output(component_id="poster_graph", component_property='figure'),
    
    Input(component_id="ip_seed", component_property="value"),
    Input(component_id="ip_plotrows", component_property="value"),
    Input(component_id="ip_plotcols", component_property="value"),
    Input(component_id="dd_sort", component_property="value"),
    # Input(component_id="filtered_wt_intermediate", component_property="data"),
    Input(component_id="filtered_wf_intermediate", component_property="data"),    

)
def update_tab3(value_seed, value_pr, value_pc,value_sort,  filtered_wf_data_json):
    # filtered_wt_data_idx = pd.read_json(filtered_wt_data_json).iloc[:, 0].tolist()
    filtered_wf_data_idx = pd.read_json(filtered_wf_data_json).iloc[:, 0].tolist()
    # filtered_wt_data = data_windturbines[data_windturbines.id.isin(filtered_wt_data_idx)]
    filtered_wf_data = data_windfarms[data_windfarms.WFid.isin(filtered_wf_data_idx)]

    poster_figure =  plot_wf_poster(data_windturbines, filtered_wf_data,  seed = value_seed, plot_col= value_pc, plot_rows =value_pr, sorting_condition= value_sort)
    # poster_figure.show()
    return  poster_figure

# Send Error Callback 
@app.callback(
    Output("popover_content", "children"), 
    Output("popover-alt-target", "style"),
    Input(component_id="filter_application_wts", component_property="children"),   
    Input(component_id="filter_application", component_property="children"),
    Input(component_id="ip_plotrows", component_property="value"),
    Input(component_id="ip_plotcols", component_property="value"),
    Input(component_id="tabs", component_property="value"),
)
def update_error(input_string_wt, input_string_wf, pr, pc, tabvalues):
    if (str(input_string_wt) == "0"):
        return "There are no turbines to the applied filters!", {'backgroundColor':'#E55934', 'border':'1px solid #E55934', "color":"#fff"}
    elif((int(str(input_string_wf).replace(".", "")) < pr*pc) and (tabvalues   == "tab-3")):
        return "Less wind farms than traces for Poster plot!", {'backgroundColor':'#E55934', 'border':'1px solid #E55934', "color":"#fff"}
    else:
        return "", {'display':'none'} 



if __name__ == '__main__':
    app.run_server(debug = False)
    # application.run(port=8080, debug = True)