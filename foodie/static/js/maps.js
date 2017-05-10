function initMap() {
  var uluru = {lat: 40.819741, lng: -73.950536};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 16,
    center: uluru
  });
  var marker = new google.maps.Marker({
   position: uluru,
   map: map
  });
}