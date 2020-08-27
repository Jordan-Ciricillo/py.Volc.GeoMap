#Folium for map objects
import folium
import pandas

#base map near Seattle, WA USA because why not?
map = folium.Map(location=[47.575,-122.229], zoom_start = 6, tiles= "Stamen Terrain")

featGroup = folium.FeatureGroup(name='Volcanoes')
featGroup2 = folium.FeatureGroup(name='Population')

#import some volcano data to test and put it in a dataframe
# rip out each type into a list
data= pandas.read_csv("volc.csv")
lat_list = list(data["LAT"])
long_list = list(data["LON"])
elev_list = list(data["ELEV"])
name_list = list(data["NAME"])
type_list = list(data["TYPE"])
country_list = list(data["COUNTRY"])
location_list = list(data["LOCATION"])
status_list= list(data["STATUS"])

#format the popup frame html and allow a clickable google search
html = """
Type: %s <br>
Name: %s <br>
Height: %s m <br> 
Country: %s <br>
Location: %s <br>
<a href="https://www.google.com/search?q=%%22%s%%22+volcano" target="_blank"> Click to Google it!</a><br>
"""

#color code volcanos by height, in meters. 
def color_coder(elev):
    if elev <= 1500:
        return 'green'
    elif elev > 1500 and elev <= 3000:
        return 'orange'
    else:
        return 'red'
    

#for loop to add all the items to the feature group
for lat, lon, ele, name, typev, country, loc, in zip(lat_list, long_list, elev_list, name_list, type_list, country_list, location_list):
    iframe = folium.IFrame(html=html % (typev, name, str(ele), country, loc,name), width=225, height=150)
   # featGroup.add_child(folium.Marker(location=[lat, lon], popup=folium.Popup(iframe), icon=folium.Icon(color=color_coder(ele))))
    featGroup.add_child(folium.CircleMarker(location=[lat, lon], popup=folium.Popup(iframe), radius=6,
     fill_color=color_coder(ele), color = 'grey', fill_opacity=0.75, weight= 2))


#import population data for a polygon overlay
#lambda the fill colors
featGroup2.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'yellow' if x ["properties"]["POP2005"]< 15000000
 else {'fillColor':'green'} if x["properties"]["POP2005"] <= 35000000 else 'red'}))


#add all the items from the feature grouping and save them
#some weird folium bug where the geojson data overrides markers entirely when called second..?
map.add_child(featGroup2)
map.add_child(featGroup)

map.add_child(folium.LayerControl())
map.save("Mappy.html")
