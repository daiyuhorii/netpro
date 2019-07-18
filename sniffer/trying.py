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
dendai = [{"IP": "133.14.0.0", "latitude": "35.69", "longitude": "139.69"}
        ]

# s_latitude = srcの緯度,d_latitude = dstの緯度
info_a = [{"src":"133.14.0.0","dst":"8.8.8.8","s_latitude":"","s_longitude":"","d_latitude":"","d_longitude":""}]


print(dendai[0])
for i in range(len(info_a)):
    try:
        response = reader.city(info_a[0]["src"])
        info_a[0]["s_latitude"] = response.location.latitude
        info_a[0]["s_longitude"] = response.location.longitude
        response = reader.city(info_a[0]["dst"])
        info_a[0]["d_latitude"] = response.location.latitude
        info_a[0]["d_longitude"] = response.location.longitude
    except geoip2.errors.AddressNotFoundError:
        print("error!")

reader.close()

print(info_a)
# generate map
m = folium.Map(location=[str(dendai[0]["latitude"]), str(dendai[0]["longitude"])],
               tiles='Stamen Terrain',
               zoom_start=2)

tooltip = "Click me!"
# 電大のみ個別でマッピング
folium.Marker(location=[str(dendai[0]["latitude"]), str(dendai[0]["longitude"])],
              popup="IP:" + str(dendai[0]["IP"]) + "\n緯度:" + str(dendai[0]["latitude"]) + "\n経度:" + str(dendai[0]["longitude"])
                    + "ここが電大", icon=folium.Icon(color='green'), tooltip=tooltip).add_to(m)

for i in range(len(info_a)):
    # dst がdbにないとき
    if info_a[i]["d_latitude"] == "":
        print("skipped")
    # src mapping
    folium.Marker(location=[info_a[i]["s_latitude"], info_a[i]["s_longitude"]],
                  popup='src:' + str(info_a[i]["src"]) + "\n緯度:" + str(info_a[i]["s_latitude"]) + "\n経度:" + str(info_a[i]["s_longitude"]),
                  icon=folium.Icon(color='blue'),tooltip=tooltip).add_to(m)

    # dst mapping
    folium.Marker(location=[info_a[i]["d_latitude"], info_a[i]["d_longitude"]],
                  popup='dst:' + str(info_a[i]["dst"]) + "\n緯度:" + str(info_a[i]["d_latitude"]) + "\n経度:" + str(
                      info_a[i]["d_longitude"]),
                  icon=folium.Icon(color='red'),tooltip=tooltip).add_to(m)

    locations = [ [float(info_a[i]["s_latitude"]), float(info_a[i]["s_longitude"])],[float(info_a[i]["d_latitude"]), float(info_a[i]["d_longitude"])]]

    folium.PolyLine(locations=locations).add_to(m)
    folium.CircleMarker(location=(float(info_a[i]["d_latitude"]),float(info_a[i]["d_longitude"])),
                                fill_color='blue', number_of_sides=3, radius=5,rotation=10).add_to(m)



m.save('test1.html')
url = ""
url += os.getcwd() + r"\test1.html"
browser = webbrowser.get()
browser.open(url)
