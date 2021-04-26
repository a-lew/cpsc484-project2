$(document).ready(function() {
    twod.start();
    frames.start();
    status_app.start();
    artwork.start();
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

var artwork = {
  socket: null,
  start: function() {
    var url = "ws://" + location.host + "/artwork";
    artwork.socket = new WebSocket(url);
    artwork.socket.onmessage = function(event) {
      artwork.process(JSON.parse(event.data));
    }
  },

  process: function(data) {
    $('img.artwork').attr("src", data.primaryImageSmall);
    $('span.name').html(data.title);
    $('span.author').html(data.artistDisplayName)
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
  }
};
