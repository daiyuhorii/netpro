import os
import socket
import webbrowser
import folium
import geoip2.database
# from venv.Scripts.netpro_Kadai import IPsniff


reader = geoip2.database.Reader("GeoLite2-City.mmdb")
hostIP = socket.gethostbyname(socket.gethostname())
IP_array = ["169.254.17.203", "133.1.0.0", "8.8.8.8", "2.2.2.2", "54.70.157.111"]
latitudes = []
longitudes = []
# 電大IP中心とする
info = [{"IP": "133.14.0.0", "latitude": "35.69", "longitude": "139.69"}
        ]


print(info[0])
for i in range(len(IP_array)):
    try:
        response = reader.city(IP_array[i])
        print(IP_array[i], response.location.latitude, response.location.longitude)
        latitudes.append(response.location.latitude)
        longitudes.append(response.location.longitude)
    except geoip2.errors.AddressNotFoundError:
        print("error!")

reader.close()

# generate map
m = folium.Map(location=[str(info[0]["latitude"]), str(info[0]["longitude"])],
               tiles='Stamen Terrain',
               zoom_start=2)

tooltip = "Click me!"
folium.Marker(location=[str(info[0]["latitude"]), str(info[0]["longitude"])],
              popup="IP:" + str(info[0]["IP"]) + "\n緯度:" + str(info[0]["latitude"]) + "\n経度:" + str(info[0]["longitude"])
                    + "ここが電大", icon=folium.Icon(color='green'), tooltip=tooltip).add_to(m)

for i in range(len(longitudes)):
    folium.Marker(location=[latitudes[i], longitudes[i]],
                  popup='IP:' + str(IP_array[i]) + "\n緯度:" + str(latitudes[i]) + "\n経度:" + str(longitudes[i]),
                  tooltip=tooltip).add_to(m)

m.save('test1.html')
url = ""
url += os.getcwd() + r"\test1.html"
browser = webbrowser.get()
browser.open(url)
