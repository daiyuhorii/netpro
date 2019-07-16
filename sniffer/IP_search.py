import geoip2.database
import folium
import webbrowser
import os

reader = geoip2.database.Reader("GeoLite2-City.mmdb")
IP_array = ["133.1.0.0", "8.8.8.8", "2.2.2.2","54.70.157.111"]
latitudes = []
longitudes = []
for i in range(len(IP_array)):
    response = reader.city(IP_array[i])
    print(IP_array[i],response.location.latitude,response.location.longitude)
    latitudes.append(response.location.latitude)
    longitudes.append(response.location.longitude)

reader.close()

# generate map
m = folium.Map(location=[latitudes[0], longitudes[0]],
                           tiles='Stamen Terrain',
                           zoom_start=2)
tooltip = "Click me!"
for i in range(len(IP_array)):
    folium.Marker(location=[latitudes[i], longitudes[i]],
                         popup="IP:"+str(IP_array[i])+"\n緯度:"+str(latitudes[i])+"\n経度:"+str(longitudes[i]),

                         tooltip=tooltip).add_to(m)

m.save('test1.html')
url = ""
url += os.getcwd() + r"\test1.html"
browser = webbrowser.get()
browser.open(url)
