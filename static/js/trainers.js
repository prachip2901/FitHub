// Example trainer data (replace with dynamic backend data if needed)
const trainers = [
  {name:"Rajat Upadhyay", specialty:"Yoga", lat:23.022505, lng:72.571362},
  {name:"Priya Sharma", specialty:"HIIT", lat:23.025, lng:72.575},
  {name:"Amit Patel", specialty:"Weight Loss", lat:23.019, lng:72.568}
];

const nearbyCarousel = document.getElementById("nearbyCarousel");

// Create card element
function createCard(trainer, distanceText){
    const card = document.createElement("div");
    card.className = "card m-2 p-3";
    card.style.minWidth = "200px";
    card.innerHTML = `
        <h5 class="card-title">${trainer.name}</h5>
        <p class="card-text">${trainer.specialty}</p>
        <small>${distanceText}</small>
    `;
    return card;
}

// Distance calculation (km)
function getDistance(lat1, lng1, lat2, lng2){
    const R = 6371;
    const dLat = (lat2-lat1)*Math.PI/180;
    const dLng = (lng2-lng1)*Math.PI/180;
    const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLng/2)**2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return (R*c).toFixed(1);
}

// Update Nearby Carousel
function updateNearbyCarousel(){
    nearbyCarousel.innerHTML = "";
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(pos => {
            const userLat = pos.coords.latitude;
            const userLng = pos.coords.longitude;

            trainers.map(t => ({...t, distance: getDistance(userLat,userLng,t.lat,t.lng)}))
                    .sort((a,b)=>a.distance-b.distance)
                    .forEach(t => nearbyCarousel.appendChild(createCard(t, `${t.distance} km away`)));
        }, err => {
            nearbyCarousel.innerHTML = '<p class="text-muted">Location access denied.</p>';
        });
    } else {
        nearbyCarousel.innerHTML = '<p class="text-muted">Geolocation not supported.</p>';
    }
}

// Nearby Google Maps button
document.getElementById("nearbyBtn").addEventListener("click", function(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(pos => {
            const userLat = pos.coords.latitude;
            const userLng = pos.coords.longitude;
            const url = `https://www.google.com/maps/search/trainers+near+me/@${userLat},${userLng},14z`;
            window.open(url, "_blank");
        }, err => {
            alert("Location access denied or unavailable.");
        });
    } else {
        alert("Geolocation not supported by your browser.");
    }
});

// Filter/Search
function filterCarousels(){
    const search = document.getElementById("trainerSearch").value.toLowerCase();
    const spec = document.getElementById("trainerSpecFilter").value;

    document.querySelectorAll("#nearbyCarousel .card")
      .forEach(card => {
        const name = card.querySelector(".card-title").innerText.toLowerCase();
        const sp = card.querySelector(".card-text").innerText.toLowerCase();
        card.style.display = (name.includes(search) && (spec==="all" || sp.includes(spec))) ? "" : "none";
      });
}

// Event listeners
document.getElementById("trainerSearch").addEventListener("input", filterCarousels);
document.getElementById("trainerSpecFilter").addEventListener("change", filterCarousels);

// Initial load
updateNearbyCarousel();
