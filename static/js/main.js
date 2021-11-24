var socket = io.connect(window.location.protocol + '//' + document.domain + ':' + location.port);

socket.on('connect', function(){
    console.log("Connected...!", socket.connected)
});


var canvas = document.getElementById('canvas');
if(canvas.getContext('2d'))
{
var context = canvas.getContext('2d');
}

const video = document.querySelector("#videoElement");

video.width = 400;
video.height = 300;


if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function (err0r) {

    });
}
var mode = 0

function normal_background(){
    mode = 0
}

function remove_background(){
    mode = 1
}

function blur_background(){
    mode = 2
}

function change_background(){
    mode = 3
}


const FPS = 10;
setInterval(() => {
    width=video.width;
    height=video.height;
    context.drawImage(video, 0, 0, width , height );
    var data = canvas.toDataURL('image/jpeg', 0.5);
    context.clearRect(0, 0, width,height );
    socket.emit('image', {data:data, mode:mode});
}, 1000/FPS);

socket.on('response_back', function(image){
        photo.setAttribute('src', image );

});