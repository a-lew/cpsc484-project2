$(document).ready(function() {
    twod.start();
    frames.start();
    status_app.start();
});

var twod = {
  socket: null,
  start: function() {
    var url = "ws://" + location.host + "/twod";
    twod.socket = new WebSocket(url);
    twod.socket.onmessage = function(event) {
      twod.process(JSON.parse(event.data));
    }
  },

  process: function(data) {
    $('img.twod').attr("src", 'data:image/pnjpegg;base64,'+data.src);
  }
};

var frames = {
  socket: null,
  start: function() {
    var url = "ws://" + location.host + "/frames";
    frames.socket = new WebSocket(url);
    frames.socket.onmessage = function(event) {
      frames.process(JSON.parse(event.data));
    }
  },

  process: function(data) {
    $('p.framelog').html(data.ts)
//    console.log(data)
  }
};

var status_app = {
  socket: null,
  start: function() {
    var url = "ws://" + location.host + "/status_app";
    status_app.socket = new WebSocket(url);
    status_app.socket.onmessage = function(event) {
      status_app.process(event.data);
    }
  },

  process: function(data) {
//    console.log(data)
    if (parseInt(data) > 3) {
      $('p.statuslogger').html("BIG STATUS");
      $('img.twod').show();
    } else{
      $('p.statuslogger').html("LITTLE STATUS")
      $('img.twod').hide();
    }
  }
};
