$(document).ready(function() {
    twod.start();
    frames.start();
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
    console.log(data)
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
    if (data.status == 'Idle') {
      $('h1.name').text('Idle');
      // we want to have a blank screen here
    } else if (data.status == 'Align') {
      $('h1.name').text('Align');
    } else if (data.status == 'Capture') {
      $('h1.name').text('Capture');
      $('h2.artistDisplayName').html('');
    } else if(data.status == 'Display') {
      $('img.artwork').attr("src", data.artwork.primaryImageSmall);
      $('h1.name').text(data.artwork.title);
      $('h2.artistDisplayName').text(data.artwork.artistDisplayName);
      $('p.objectDate').text(data.artwork.objectDate)
      $('p.medium').text(data.artwork.medium)
      $('p.repository').text(data.artwork.repository)
    }

  }
};
