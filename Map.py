from nicegui import ui
import asyncio

# Define the initial map
leaflet_html = """
<div id="map" style="height: 100vh;"></div>
<script>
var map = L.map('map').setView([36.1699, -115.1398], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
var carIcon = L.icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/743/743131.png',
  iconSize: [40,40],
  iconAnchor: [20,20]
});
window.carMarker = L.marker([36.1699, -115.1398], {icon: carIcon}).addTo(map);
</script>
"""

# Add the map
ui.add_body_html(leaflet_html)

# Function to move the car (controlled by Python)
async def move_car():
    coords = [
        (36.1699, -115.1398),
        (36.1710, -115.1409),
        (36.1722, -115.1425),
        (36.1730, -115.1442),
    ]
    for lat, lon in coords:
        ui.run_javascript(f"carMarker.setLatLng([{lat}, {lon}]); map.panTo([{lat}, {lon}]);")
        await asyncio.sleep(1)

ui.button('Start Ride', on_click=move_car)

ui.run(native=True)
