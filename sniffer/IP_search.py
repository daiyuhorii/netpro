import os
import socket
import webbrowser
import folium
import geoip2.database
import sniff


reader = geoip2.database.Reader("./GeoLite2-City/GeoLite2-City.mmdb")

# 電大IP中心とする
info = [{"IP": "133.14.0.0", "latitude": "35.69", "longitude": "139.69"}
        ]


def main():
    # sniff() returns dict {src: [dst, upper protocols(TCP/UDP)]}
    inputs = sniff.sniff()
    print(inputs)

    data = list()

    for src, dst_proto in inputs.items():
        print("src:", src, "lists:", dst_proto)
        try:
            src_response = reader.city(src)
            if("192.168" in dst_proto[0]):
                dst_response = reader.city("133.14.0.0")
            else:
                dst_response = reader.city(dst_proto[0])
            s_latitude = src_response.location.latitude
            s_longitude = src_response.location.longitude
            d_latitude = dst_response.location.latitude
            d_longitude = dst_response.location.longitude
            comm = {"src": src, "dst": dst_proto[0],
                    "s_latitude": s_latitude, "s_longitude": s_longitude,
                    "d_latitude": d_latitude, "d_longitude": d_longitude,
                    "protocol": dst_proto[1]}
            data.append(comm)
        except geoip2.errors.AddressNotFoundError:
            print("error!")
            continue
        except ValueError:
            print("Invalid IP")
            continue

    reader.close()
    print("DATA\n")
    print(data)
    # generate map
    m = folium.Map(location=[str(info[0]["latitude"]), str(info[0]["longitude"])],
                   tiles='Stamen Terrain',
                   zoom_start=2)

    tooltip = "Click me!"
    for i in range(len(data)):
        # dst がdbにないとき
        if data[i]["d_latitude"] == "":
            print("skipped")
        # src mapping
        folium.Marker(location=[data[i]["s_latitude"], data[i]["s_longitude"]],
                      popup='src:' + str(data[i]["src"]) +
                            "\n緯度:\n" + str(data[i]["s_latitude"]) +
                            "\n経度:\n" + str(data[i]["s_longitude"]),
                      icon=folium.Icon(color='blue'), tooltip=tooltip).add_to(m)

        # dst mapping
        folium.Marker(location=[data[i]["d_latitude"], data[i]["d_longitude"]],
                      popup='dst:' + str(data[i]["dst"]) +
                            "\n緯度:\n" + str(data[i]["d_latitude"]) +
                            "\n経度:\n" + str(data[i]["d_longitude"]),
                      icon=folium.Icon(color='red'), tooltip=tooltip).add_to(m)

        locations = [[float(data[i]["s_latitude"]), float(data[i]["s_longitude"])],
                     [float(data[i]["d_latitude"]), float(data[i]["d_longitude"])]]

        folium.PolyLine(locations=locations, popup="protocol: " + data[i]['protocol']).add_to(m)

    m.save('test1.html')
    url = ""
    url += os.getcwd() + r"\test1.html"
    browser = webbrowser.get()
    browser.open(url)

if __name__ == '__main__':
    main()