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
				travelMode: google.maps.TravelMode['DRIVING']
			}, function(response,status){
				if (status === google.maps.DirectionsStatus.OK){
					var directionDisplay = new google.maps.DirectionsRenderer({
						map:map,
						directions: response,
						draggable: true,
						polylineOptions:{
							strokeColor: 'green'
						}
					});
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

