$(document).ready(function() {
    twod.start();
    frames.start();
    artwork.start();
});

var port = ":6677"

var twod = {
  socket: null,
  start: function() {
    var url = "ws://" + location.hostname + port + "/twod";
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
    var url = "ws://" + location.hostname + port + "/frames";
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
    var url = "ws://" + location.hostname + port + "/artwork";
    artwork.socket = new WebSocket(url);
    artwork.socket.onmessage = function(event) {
      artwork.process(JSON.parse(event.data));
    }
  },

  process: function(data) {
    if (data.status == 'Idle') {
      $('img.artwork').attr("src", "idle.svg");
    } else if (data.status == 'Align') {
      if (data.nudge == 'Left') {
        $('img.artwork').attr("src", "align_left.svg");
      } else if (data.nudge == 'Right') {
        $('img.artwork').attr("src", "align_right.svg");
      } else if (data.nudge == 'Forward') {
        $('img.artwork').attr("src", "align_forward.svg");
      } else if (data.nudge == 'Backward') {
        $('img.artwork').attr("src", "align_backward.svg");
      } else {
        $('img.artwork').attr("src", "idle.svg");
      }
    } else if (data.status == 'Capture') {
      $('img.artwork').attr("src", "capture.svg");
      $('h1.name').text("Searching...");
      $('h2.artistDisplayName').text("...");
      $('p.objectDate').text("...");
      $('p.medium').text("...");
      $('p.repository').text("...");
    } else if(data.status == 'Display') {
      $('img.artwork').attr("src", data.artwork.primaryImageSmall);
      $('h1.name').text(data.artwork.title);
      $('h2.artistDisplayName').text(data.artwork.artistDisplayName);
      $('p.objectDate').text(data.artwork.objectDate);
      $('p.medium').text(data.artwork.medium);
      $('p.repository').text(data.artwork.repository);
    }

  }
};
