from exif import Image
import folium
import glob


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
         decimal_degrees = -decimal_degrees
    return decimal_degrees

def image_coordinates(image_path):
    coords = ""
    with open(image_path, 'rb') as src:
        img = Image(src)
    if img.has_exif:
        try:
            img.gps_longitude
            coords = (decimal_coords(img.gps_latitude,
                      img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                      img.gps_longitude_ref))
        except AttributeError:
            print (image_path, " No Coordinates")
    else:
        print (image_path, "has no EXIF information")
    return coords


def create_map(coordinates_origin, path_images):
    # We load all images from our images folder
    image_path_list = glob.glob(f"{path_images}/*.*")

    # We create a list with coordiantes of the image and the path of that image
    coordinate_path_list = []
    for img_path in image_path_list:
        coordinates = image_coordinates(img_path)
        coordinate_path_list.append([coordinates, img_path])

    # We create the map
    TravelMap = folium.Map(location=coordinates_origin, zoom_start=4)

    for coord_path in coordinate_path_list:
        if coord_path[0]:
            name = "Travel pics"
            icono = folium.Icon(color="lightgreen",
                         opacity=0.3,
                         icon="glyphicon glyphicon-picture",
                         icon_color="black",
                         )
            # Define html inside marker pop-up
            travel_html = folium.Html(
                f"""<p style="text-align: center;"><b><span style="font-family: Didot, serif; font-size: 18px;">{name}</b></span></p>
            <p style="text-align: center;"><img src={coord_path[1]} width="200px" height="200px">
            """, script=True)

            # Create pop-up with html content
            popup = folium.Popup(travel_html, max_width=220)
            # Create marker using instance of custom_icon and popup.
            custom_marker = folium.Marker(location=coord_path[0],
                                          icon=icono, tooltip=name, popup=popup)

            custom_marker.add_to(TravelMap)
    return TravelMap