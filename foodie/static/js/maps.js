function initMap() {
  var restaurant = {lat: 40.819741, lng: -73.950536};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 16,
    center: restaurant
  });

  var marker = new google.maps.Marker({
   position: restaurant,
   map: map
  });

  document.getElementById('zoom-to-area').addEventListener('click',function(){
  	// zoomToArea()
  	displayDirections()
  });

function displayDirections(){
			var directionService = new google.maps.DirectionsService;
			var address = document.getElementById('zoom-to-area-text').innerHTML;
			directionService.route({
				origin:restaurant,
				destination: address,
				travelMode: google.maps.TravelMode['DRIVING'],
				provideRouteAlternatives: true
			}, function(response,status){
				marker.setMap(null);
				if (status === google.maps.DirectionsStatus.OK){
					var polycolour = "";
      				var Opacity = 0;
					for (var i = 0, len = response.routes.length; i < len; i++) {
					if (i == 0) {
					    polycolour = "#008000";
					     Opacity = 6;
					 }
					  else {
					     polycolour = "#b30000";
					     Opacity = 2;
					}
					var directionDisplay = new google.maps.DirectionsRenderer({
						map:map,
						directions: response,
						routeIndex: i,
						draggable: true,

						polylineOptions:{
							strokeColor: polycolour,
            				strokeWeight: Opacity,
            				stokeOpacity: Opacity
						}
					});
				}
				}else{
					window.alert('Directions request failed due to '+ status);
				}
			});
		}
function zoomToArea(){
	var geocoder = new google.maps.Geocoder();
	var address = document.getElementById('zoom-to-area-text').innerHTML;
	if (address == ''){
		window.alert('Please enter an address');
	}else {
		geocoder.geocode(
		{
			address:address,
			componentRestrictions:{locality: 'New York'}
		}, function(results, status){
			if (status == google.maps.GeocoderStatus.OK){
				// var marker = new google.maps.Marker({
				// 	position: results[0].geometry.location,
				// 	map: map,
				// 	title: 'This is it'
				// });
				map.setCenter(results[0].geometry.location);
				map.setZoom(15);
			}else{
				window.alert('Could not find the address');
			}
		});
	}
  }
}

