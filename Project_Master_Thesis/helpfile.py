import numpy as np
from numpy import random
import pandas as pd
# from geopy.distance import great_circle as GRC
from sklearn.cluster import DBSCAN, dbscan
from pyproj import Proj, transform
import math
import plotly.express as px
import random
import requests
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry
import time
import turf
# Test Datas
# y = [3.3701922269319766, 3.237467945418757, 3.105235073663607, 2.9750043413778258, 2.889362294743478, 2.7526182346673522, 2.617372712672477, 2.4736112976452205, 2.3298490420174858, 2.189084595532222, 2.045812823976121, 1.9015444712704266, 1.751747129766045, 1.6064698480940933, 1.4501581801914654, 1.3078778742265058]
# x =[0.7955648126298911, 0.9347011696936534, 1.0722549957390584, 1.2134080335963517, 1.4031656952047342, 1.544614080192332, 1.6831969111972285, 1.819900759448501, 1.9599161272417405, 2.096569597320922, 2.233597228430881, 2.3766492793292855, 2.5239181594060938, 2.6687380340536038, 2.8153555966673594, 2.975302944141731]

# Sample IDs
sample_ids = ['7797671729', '2374866935', '1027891959', '6056970085', '1575947951', '1930587642', '2624031665', '3939570641', '5150138290', '8912221984', '272115329', '5082239069', '3262630692', '6546022824', '9215212174', '2948957348', '4719508428', '1424247178', '5535388939', '1920015927', '4985361720', '8410327497', '2285931181', '5915275855', '8434799395', '1617174760', '5837820554', '3020446236', '7352754819', '1415560110', '7855166538', '5082238677', '7764697641', '7688155199', '2739324469', '6128264237', '4560858145', '5176477776', '9296174813', '7215879820', '5114920853', '924698044', '4476561380', '4761934277', '4449599697', '1624375149', '6491488541', '9408066448', '1151933960', '1166963831', '1743181460', '6561731217', '9095209607', '6970348767', '1884596285', '3992544940', '1726892515', '3595103622', '9218202692', '4746122250', '8434018748', '7764682681', '6568686686', '6988564591', '7004017692', '2595845174', '1151741950', '2292506785', '8964739984', '272117176', '704986376', '1097919722', '3148283184', '3449172218', '752697913', '6793250174', '6783552185', '1770064089', '3371393364', '2499713645', '4955317814', '1740730561', '7904341206', '272115257', '3147424752', '1589536660', '894883357', '1026531209', '1909034421', '8713424226', '8262020276', '2186484474', '1013654504', '5163932377', '3148281819', '2921118179', '2587564185', '9359474095', '7771189335', '2122783073', '8651194089', '3673506163', '8419619767', '2345935711', '8912222628', '1113476082', '8848619787', '4498235599', '7769579600', '1589537733', '4390048794', '7261666354', '1471726920', '3112173129', '5163920913', '7492081190', '7622995011', 
'1673650287', '8654458008', '944348982', '5313665881', '8428064903', '7653793814', '6939112380', '1853815166', '4620749627', '9312315959', '3056988700', '2186484372', '1875102546', '2056840086', '5389703959', '9111843626', '1997782975', '5163917443', '7252047805', '1996228900', '6794573244', '7765272151', '3894100032', '5095801813', '2011013710', '6521984906', '7252092073', '1122301582', '8460998434', '1700585282', '9104211066', '3736539990', '1809591925', '6518836108', '1664273915', '1048501886', '7786710722', '3047666183', '7680574748', '258215991', '6988600992', '7260626676', '6480782432', '3733258889', '4584736479', '8419637548', '1165440089', '6238232201', '3753437234', '1680486050', '3107479108', '8118634791', '1662991451', '8419736029', '8672878884', '7607458643', '1815489004', '1718145051', '2712095779', '2029842544', '6996871541', '8929120508', '2419129519', '5025334393', '6581574119', '4706019018', '5888421476', '3388175864', '1968567051', '2615869809', '6518836116', '1777427884', '9104186716', 
'3260713756', '6524096863', '4262091946', '2316313228', '3214444081', '6651687370', '3655658971', '3452090278', '8458247967', '5891088229', '5995908666', '8391149134', '5923385688', '270357250', '3161770047', '1589534393', '2417452822', '9117542634', '2048337774', '6035490207', '1384683288', '5849748944', '5146621888', '2441125212', '2417980229', '1151742604', '4589467464', '3244610826', '1416409694', '3182337193', '5492542110', '6318909312', '5432935507', '7215865632', '4840380430', '1167267110', '1025784601', '1053727024', '2451031318', '5890648034', '7764745433', '6623032214', '9360391597', '9121166721', '4584807425', '7215848611', '1791231486', '1181453712', '1832298729', '2264948609', '3500846823', '2510245918', '5566853405', '5891092006', '5083690844', '4732541721', '5043825718', '2022677547', '6937408708', '1437732154', '8320783057', '1298230116', '8936100386', '7041615621', '1601210036', '1849367972', '5341756159', '4729571063', '3522137649', '6104164656', '2154680362', '1615750563', '6965087369', '8434780991', '6616196348', '1840150948', '1455124921', '6322530119', '2340723405', '3592929764', '9145778033', '5082238001', '3692959361', '6518027465', '2730052278', '6471038549', '1221615955', '3439395633', '9231166817', '5591749272', '5308533392', '5150138312', '2966451671', '6802898221', '5163922664', '1607651980', '1693089065', '7040783889', '6528146185', '4009650931', '2302355877', '3898819504', '6990139676', '5163913327', '7924447348', '919304640', '7455108676', '1762991778', '1919822384', '7850419600', '1684638771', '2577027694', '2579714987', '8508583076', '8403337904', '3435388009', '2339113473', '452073517', '5080016996', '922236317', '2363140337', '7928623639', '4348680640', '3812721808', '2275396340', '8410440585', '2382531607', '7286426642', '8434368421', '2581019409', '6503568875', '5163912807', '7033721313', '3815264055', '2666097407', '7223278655', '942137868', '3327065203', '8187010321', '6992343190', '3753437267', '272115430', '8242683338', '6469541658', '2364227353', '8410379160', '1545900356', '2451004332', '4210817900', '4201689533', '6401976083', '1551290006', '2587236541', '8303074815', '5163913596', '1244655330', '1290372499', '8677949828', '5556028346', '8014031364', '5163922637', '2954983745', '2217417101', '7781781835', '303118651', '8425257278', '7819899516', '7819946291', '6804257478', '6470441916', '5018774870', '7706763954', '2499964194', '3449172305', '6991236911', '2132626411', '3255957762', '9060109350', '4929076063', '923875694', '9159399039', '5491076659', '1172112932', '6764954007', '2139148786', '1589537160', '1494285809', '5888425052', '807724123', '3557688209', '388217544', '1111612156', '8912221124', '2349681507', '7254666931', '8425208004', '6948802301', '2577027775', '2130794151', '1589536069', '2200423687', '1832321873', '5083690926', '940891707', '7112438021', '1097199277', '1724595511', '3239588184', '5701195518', '3373515263', '5838427831', '2507732948', '7947154167', '2294939329', '8526073818', '7839672631', '1740079614', '8798263428', '7260642669', '3371302713', '2906431235', '4035524803', '272130606', '5163928361', '8729285093', '3883121706', '923688762', '5566853434', '7171036554', '2788572756', '9210579502', '2726824668', '3100780424', '1614866793', '1872676122', '8912221734', '3163247787', '8725467246', '4296681420', '8729456983', '303782911', '1928443492', '9374967509', '9296230326', '4984739922', '1437732252', '3768786138', '2731749816', '924698194', '7816690513', '3768743074', '7093405395', '313798922', '7340344056', '3041025463', '8246213025', '1624392045', '6000766202', '7258941108', '509397369', '8419657574', '6988559483', '1872676188', '1151725070', '4031834598', '8963319270', '1700585001', '6151336831', '3500847307', '3148285434', '3289327499', '1589534545', '3318241737', '2998393243', '5002387899', '7856839036', '6053446742', '8770180008', '1117047106', '4198277128', '331106995', '1664214450', '8912186655', '3501160839', '7688130957', '2509419786', '3238684168', '5715077298', '7764554550', '3750344359', '939559883', '6562788952', '3427533937', '928693506', '8099096704', '4562209361', '2277532280', '5364573965', '7234098553', '6358676719', '5932632147', '3449173774', '3768743082', '6795253605', '7283894536', '2085679560', '7764532648', '3067226335', '9104892195', '8715595726']
random.seed(25)
random.shuffle(sample_ids)


# projection to azithumal equidistance
def proj_to_wf_center(windFarm):
    windFarm.loc[:,"lat"] = pd.to_numeric(windFarm.loc[:,"lat"])
    windFarm.loc[:,"lon"] = pd.to_numeric(windFarm.loc[:,"lon"])
    # # Get center of park as 0, 0 point for projection
    lat_0 = np.mean(windFarm["lat"])
    lon_0 = np.mean(windFarm["lon"])
    projected = transform(Proj(init='epsg:4326'), Proj(proj='aeqd', ellps='WGS84', datum='WGS84', lat_0=lat_0, lon_0=lon_0, units='km'),  windFarm["lon"], windFarm["lat"])
    df_proj = pd.DataFrame(np.c_[projected[0], projected[1]])
    df_proj.columns = ["x", "y"]
    return df_proj

## Project coordinates with Mollweide Projection at 1 km Resolution
def map_projection(windData):
    windData.loc[:,"lat"] = pd.to_numeric(windData.loc[:,"lat"])
    windData.loc[:,"lon"] = pd.to_numeric(windData.loc[:,"lon"])
    # projected = transform(Proj(init='epsg:4326'), Proj(proj='moll', units='km'),  windData["lon"], windData["lat"])
    projected = transform(Proj(init='epsg:4326'), Proj(proj='eck4', units='km'),  windData["lon"], windData["lat"])
    df_proj = pd.DataFrame(np.c_[projected[0], projected[1]])
    df_proj.columns = ["x", "y"]
    return df_proj
# Distance Functions for Coordinates 
# def dist(p1, p2):
#     return GRC(p1 ,p2).m



def dbscan_func(eps, min_samples, data, storefile = True):
# Set Parameters for DBSCAN clustering
    # eps_smalldist = 0.8 #30 m: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
    # min_samples_smalldist = 2 # min number of turbines in a neighborhood for a point to be considered as a core point
    # fit dbscan model on data
    clustering_smalldistance = DBSCAN(eps=eps, min_samples=min_samples, algorithm = "kd_tree").fit(data[["lon_proj", "lat_proj"]])
    # clustering_smalldistance = DBSCAN(eps=0.03, min_samples=2, algorithm = "kd_tree").fit(data[["lon_proj", "lat_proj"]])

    # Predicted Wind Farm data frame
    groups_smalldistance = clustering_smalldistance.labels_#
    df = data.assign(WFid =groups_smalldistance)
    # df["WFid"] = groups_smalldistance

    # store unique farm ids and g
    farm_ids = np.unique(clustering_smalldistance.labels_)
    df_close_turbines = df[df["WFid"] != -1]
    df_single_turbines = df[df["WFid"] == -1]
    print("Number of Windfarms: " + str(len(farm_ids)-1))
    print("Number of grouped turbines: " + str(len(df_close_turbines)))
    print("Number of standalone turbines: " + str(len(df_single_turbines)))
    
    # List by Farm number 
    df_grouped = df_close_turbines.groupby("WFid")

    if storefile:  
        # Create list of Wind farms with list of wind turbines as elements
        WFlist = []
        for id in farm_ids[1:]:
            wf = df_grouped.get_group(id).values[:,0:2].tolist()
            if id == -1:
                for el in wf:
                    WFlist.append(el)
            else: 
                WFlist.append(wf)

        # write js file
        import json
        with open("data/windfarms_world.js", "w") as f:
            json.dump(WFlist, f)
    
    return [df, df_grouped]

def PolyArea(x,y):
    if (len(x) == 1):
        return 1
    elif (len(x) == 2):
        p0 = [x[0], y[0]]
        p1 = [x[1], y[1]]
        return math.dist(p0, p1)
    else: 
        x = [float(m) for m in x]
        y = [float(n) for n in y]
        polycoords = np.c_[x, y]
        hull = ConvexHull(polycoords)
        return hull.volume
        # import matplotlib.pyplot as plt        
        # plt.plot(*poly.exterior.xy)
        # plt.show()
        
# calculates the density of a Windfarm per 1 km²
def WFdensity(x,y):
    n = len(x)
    area = PolyArea(x, y) 
    area_density = n/area
    return area_density ## multipy by 10^6 in order to get square km

# x = [0, 1,  0, 1]
# y = [0,0,1, 1]
# PolyArea(x, y)

def AvgDistEst(x, y):
    if (len(x) == 2):
        p0 = [x[0], y[0]]
        p1 = [x[1], y[1]]
        return math.dist(p0, p1)
    else: 
        n = len(x)
        d = WFdensity(x, y)
        return np.round(1/(pow(d, (1/n))), 5)

# compute elevation of multiple coordinates
def elevation_function(df, lat_column, lon_column):
    """Query service using lat, lon. add the elevation values as a new column."""
    i = 0 
    j = 0
    elevations = []
    for lat, lon in zip(df[lat_column], df[lon_column]):
        time.sleep(10)
        # overpass_url = "https://api.open-elevation.com/api/v1/lookup?"
        # query = '52.3625221,-0.6296027'
        query = str(lat) + "," + str(lon)
        overpass_url = "https://api.open-elevation.com/api/v1/lookup?"+"locations="+query 

        # send requests
        # response = requests.get(overpass_url,
        #                         params={"locations": query}, verify=False)
        response = requests.get(overpass_url)
        requests.get('https://api.github.com')
        # get results in json
        datajs = response.json()
        elevations.append(datajs["results"][0]["elevation"])
        i += 1
        j += 1
        if (i == 10000):
            i = 0
            print(j)
    # df_with_elev['elev_meters'] = elevations
    return elevations
# get elevations
# wt_cleaned_full = pd.read_csv("data/clustered_data.csv").iloc[1:10]
# from timeit import default_timer as timer
# start = timer()
# elev = elevation_function(wt_cleaned_full.iloc[1:2], "lat", "lon")
# end = timer()

def figures_to_html(figs, filename="dashboard.html"):
    dashboard = open(filename, 'w')
    dashboard.write("<html><head></head><body>" + "\n")
    for fig in figs:
        inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
        dashboard.write(inner_html)
    dashboard.write("</body></html>" + "\n")

def zoom_center(lons, lats):
    # """Finds optimal zoom and centering for a plotly mapbox.
    # Must be passed (lons & lats) or lonlats.
    # Temporary solution awaiting official implementation, see:
    # https://github.com/plotly/plotly.js/issues/3434
    
    # Parameters
    # --------
    # lons: tuple, optional, longitude component of each location
    # lats: tuple, optional, latitude component of each location
    # lonlats: tuple, optional, gps locations
    # format: str, specifying the order of longitud and latitude dimensions,
    #     expected values: 'lonlat' or 'latlon', only used if passed lonlats
    # projection: str, only accepting 'mercator' at the moment,
    #     raises `NotImplementedError` if other is passed
    # width_to_height: float, expected ratio of final graph's with to height,
    #     used to select the constrained axis.
    
    # Returns
    # --------
    # zoom: float, from 1 to 20
    # center: dict, gps position with 'lon' and 'lat' keys

    # >>> print(zoom_center((-109.031387, -103.385460),
    # ...     (25.587101, 31.784620)))
    # (5.75, {'lon': -106.208423, 'lat': 28.685861})
    # """
    # if lons is None and lats is None:
    #     if isinstance(lonlats, tuple):
    #         lons, lats = zip(*lonlats)
    #     else:
    #         raise ValueError(
    #             'Must pass lons & lats or lonlats'
    #         )
    
    maxlon, minlon = max(lons), min(lons)
    maxlat, minlat = max(lats), min(lats)
    center = {
        'lon': round((maxlon + minlon) / 2, 6),
        'lat': round((maxlat + minlat) / 2, 6)
    }
    
    # longitudinal range by zoom level (20 to 1)
    # in degrees, if centered at equator
    lon_zoom_range = np.array([
        0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
        0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
        47.5136, 98.304, 190.0544, 360.0
    ])
    
    margin = 3
    width_to_height =2
    height = (maxlat - minlat) * margin * width_to_height
    width = (maxlon - minlon) * margin
    lon_zoom = np.interp(width , lon_zoom_range, range(20, 0, -1))
    lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
    zoom = round(min(lon_zoom, lat_zoom), 2)

    
    return zoom, center
# zoom_center(current_wf["lon"], current_wf["lat"])
# Function that plots l random 15km² of earth surface with wind turbines contained in it
# the data must be given clustered in wind farms with respective ids and a sample subset data set
# Computes turbine density, estimated distance between turbines of every sample wind farm 
def plotRandomWF(data, wfid_column, sample_ids, l, storeFile = False, filestorage= "dashboard.html"):
    # clustered data: data containing columns ["lon_proj", "lat_proj", "id", "WFif"]
    # sample_turbines: subset data of clustered data
    # k: Number of plots, max size of sample 
    # wfid_column = "WFid_1.5"
    # data = pd.read_csv("data/clustered_data.csv")#.iloc[1:5000]
    
    clustered_data = data[["lon", "lat", "id", "lon_proj", "lat_proj","Country", "Land Cover",  wfid_column]]
    # clustered_data.columns =  = ["lon", "lat", "id", "lon_proj", "lat_proj", "WFid"]
    clustered_data["id"] = clustered_data["id"].apply(str)
    sample_turbines = clustered_data[clustered_data["id"].isin(sample_ids)]

    pts = clustered_data[["lon_proj", "lat_proj"]].apply(pd.to_numeric)
    fig_list = []
    turnout_df = clustered_data
    # for k in range(len(sample_turbines.id))
    # random.seed(27)
    # np.random.shuffle(sample_turbines)
    for k in range(l):
        
        row = sample_turbines.iloc[k]
        ll = np.array([(pd.to_numeric(row.lon_proj)-10), (pd.to_numeric(row.lat_proj)-10)])  # lower-left
        ur = np.array([(pd.to_numeric(row.lon_proj)+10), (pd.to_numeric(row.lat_proj)+10)])  # upper-right
        inidx = np.all(np.logical_and(ll <= pts, pts <= ur), axis=1)
        rand_position_data = clustered_data[inidx]
        rand_position_data["x"] = pd.to_numeric(rand_position_data.lon_proj) - np.mean(pd.to_numeric(rand_position_data.lon_proj))
        rand_position_data["y"] = pd.to_numeric(rand_position_data.lat_proj) - np.mean(pd.to_numeric(rand_position_data.lat_proj))
        rand_position_data[wfid_column] = rand_position_data[wfid_column].apply(str)

        # rand_position_data["WFid"] = rand_position_data["WFid"].apply(str)
        # rand_position_data["wfDensities"] = 0
        # rand_position_data["wfAvgDist"] = 0
        wfidx = np.unique(rand_position_data[wfid_column])
        for idx in wfidx:
            # idx = wfidx[1]
            currwf = rand_position_data[rand_position_data[wfid_column] == idx]
            # PolyArea(currwf["x"],currwf["y"] )
            currwf["wfDensities"] = str(WFdensity(list(currwf["x"]), list(currwf["y"])))
            currwf["wfAvgDist"] = str((AvgDistEst(list(currwf["x"]), list(currwf["y"]))*1000))
            currwf["NoTurbines"] = len(currwf)
            rand_position_data = rand_position_data.merge(currwf, how = "outer")
        
        noTurbines = str(len(rand_position_data))
        densityTurbines = str(WFdensity(rand_position_data["x"], rand_position_data["y"]))
        estimatedAvgDist = str((AvgDistEst(rand_position_data["x"], rand_position_data["y"])*1000))
        fig = px.scatter(rand_position_data, x  = "x", y = "y", color = wfid_column,hover_data=["NoTurbines", 'wfDensities', "wfAvgDist", "Country", "Land Cover"],  
            title="# Turbines contained: " + noTurbines + " - Density: " + densityTurbines + "/km² - Average Spacing: " + estimatedAvgDist + " m",
            labels={
                    "x": "Easting (m)",
                    "y": "Northing (m)"
                })
        fig.update_xaxes(range=[-15, 15])
        fig.update_yaxes(range=[-15, 15])
        fig_list.append(fig)
        # turnout_df = turnout_df.merge(rand_position_data)
        turnout_df = pd.concat([turnout_df, rand_position_data], axis=1, join="outer")
    
    if storeFile:
        figures_to_html(fig_list, filename=filestorage)

    return turnout_df, fig_list 

def plotRandomWF_bySampleID(data, wfid_column, sample_ids):

    # data = pd.read_csv("data/clustered_data.csv")#.iloc[1:5000]
    # wfid_column = "WFid_1.3"
    # sample_ids = 12014318
    clustered_data = data[["lon", "lat", "id", "lon_proj", "lat_proj","Country", "Land Cover", "Turbine Spacing", wfid_column]]

    sample_turbines = clustered_data[clustered_data["id"] == sample_ids]

    pts = clustered_data[["lon_proj", "lat_proj"]].apply(pd.to_numeric)
    # turnout_df = clustered_data
    # for k in range(len(sample_turbines.id))
    # random.seed(27)
    # np.random.shuffle(sample_turbines)
    
    row = sample_turbines.iloc[0]
    ll = np.array([(pd.to_numeric(row.lon_proj)-10), (pd.to_numeric(row.lat_proj)-10)])  # lower-left
    ur = np.array([(pd.to_numeric(row.lon_proj)+10), (pd.to_numeric(row.lat_proj)+10)])  # upper-right
    inidx = np.all(np.logical_and(ll <= pts, pts <= ur), axis=1)
    rand_position_data = clustered_data[inidx]
    rand_position_data["x"] = pd.to_numeric(rand_position_data.lon_proj) - np.mean(pd.to_numeric(rand_position_data.lon_proj))
    rand_position_data["y"] = pd.to_numeric(rand_position_data.lat_proj) - np.mean(pd.to_numeric(rand_position_data.lat_proj))
    rand_position_data[wfid_column] = rand_position_data[wfid_column].apply(str)
    

    wfidx = np.unique(rand_position_data[wfid_column])
    for idx in wfidx:
        # idx = wfidx[1]
        currwf = rand_position_data[rand_position_data[wfid_column] == idx]
        # PolyArea(currwf["x"],currwf["y"] )
        currwf["wfDensities"] = str(WFdensity(list(currwf["x"]), list(currwf["y"])))
        currwf["wfAvgDist"] = str((AvgDistEst(list(currwf["x"]), list(currwf["y"]))*1000))
        currwf["NoTurbines"] = len(currwf)
        rand_position_data = rand_position_data.merge(currwf, how = "outer")
        # print(currwf) 

    ### Scatter Plot 
    # noTurbines = str(len(rand_position_data))
    # densityTurbines = str(WFdensity(rand_position_data["x"], rand_position_data["y"]))
    # estimatedAvgDist = str((AvgDistEst(rand_po
    # sition_data["x"], rand_position_data["y"])*1000))
    fig = px.scatter(rand_position_data, x  = "x", y = "y", color = wfid_column,hover_data=["NoTurbines", 'wfDensities', "wfAvgDist", "Country", "Land Cover", "Turbine Spacing"],  
        # title="# Turbines contained: " + noTurbines + " - Density: " + densityTurbines + "/km² - Average Spacing: " + estimatedAvgDist + " m",
        labels={
                "x": "Easting (m)",
                "y": "Northing (m)"
            })
    fig.update_xaxes(range=[-13, 13])
    fig.update_yaxes(range=[-13, 13])
    # turnout_df = turnout_df.merge(rand_position_data)
    # turnout_df = pd.concat([turnout_df, rand_position_data], axis=1, join="outer")

    ### Map Plot 
    # mapdata = clustered_data[clustered_data[wfid_column].isin(random_wfs_ids) ]
    mapfig = px.scatter_mapbox(rand_position_data, lat="lat", lon="lon", hover_data=["NoTurbines", 'wfDensities', "wfAvgDist", "Country", "Land Cover"],
                            color_discrete_sequence=["red"], zoom=10, height=300)
    mapfig.update_layout(mapbox_style="satellite", mapbox_accesstoken="pk.eyJ1IjoiendpZWZlbGUiLCJhIjoiY2wxeTAzazJxMDcwaTNibXQ5aTRyMno0bSJ9.zPSVI0wOb_sIXGH-tgHNVw")
    mapfig.update_layout(height=1000, width=1500)

    # mapfig.show()
    return fig, mapfig



def plot_countryComparison_diffClustering(data, wfid_column ="WFid_1"):

    # data = pd.read_csv("data/clustered_data.csv")#.iloc[1:5000]
    # wfid_column = "WFid_1"


    clustered_data = data[["lon", "lat", "id", "lon_proj", "lat_proj","Country", "Land Cover",  wfid_column]]
    count_wfs = clustered_data.groupby("Country")[wfid_column].nunique().reset_index()
    count_wts = clustered_data.groupby("Country")[wfid_column].count()
    count_wfs["Number_WTs"] = count_wts.values
    count_wfs.columns = ["Country", "Number_WFs", "Number_WTs"]
    count_wfs = count_wfs.sort_values("Number_WTs", ascending=False)



    fig_count_wfs = go.Figure(data=go.Choropleth(
        locations = count_wfs["Country"],
        z = count_wfs["Number_WFs"],
        colorscale = 'Blugrn',
        text = count_wfs["Number_WTs"], 
        marker_line_width=0.5,
        colorbar_title = 'Number of wind farms per country',
        
    ))
    # fig_count_wfs.update_layout(height=700, width=900)
    
    fig_bar_counts_wfs  = go.Figure()
    fig_bar_counts_wfs.add_trace(go.Bar(
        x=count_wfs["Country"],
        y=count_wfs["Number_WTs"],
        name='#Wind Turbines',
        marker_color='indianred'
    ))
    fig_bar_counts_wfs.add_trace(go.Bar(
        x=count_wfs["Country"],
        y=count_wfs["Number_WFs"],
        name='#Wind Farms',
        marker_color='lightsalmon'
    ))
    # fig_bar_counts_wfs.update_layout(height=700, width=900)
    # fig_bar_counts_wfs.show()

    return fig_count_wfs, fig_bar_counts_wfs

