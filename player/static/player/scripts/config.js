var canvas = document.getElementById('region-canvas'),
  ctx = canvas.getContext('2d'),
  rect = {},
  drag = false;

canvas.height = canvas.width;

canvas.addEventListener('mousedown', mouseDown, false);
canvas.addEventListener('mouseup', mouseUp, false);
canvas.addEventListener('mousemove', mouseMove, false);

var latStartRatio = document.getElementById('lat-start-ratio');
var latEndRatio = document.getElementById('lat-end-ratio');
var longStartRatio = document.getElementById('long-start-ratio');
var longEndRatio = document.getElementById('long-end-ratio');

ctx.fillStyle = 'rgba(33,150,243,0.4)';

function draw() {
  ctx.fillRect(rect.startX, rect.startY, rect.w, rect.h);
  var latStart = rect.startY;
  var latEnd = rect.startY + rect.h;
  var longStart = rect.startX;
  var longEnd = rect.startX + rect.w;
  
  // make `start` smaller than `end` if required
  var temp;
  if (latStart > latEnd) {
    temp = latStart;
    latStart = latEnd;
    latEnd = temp;
  }
  if (longStart > longEnd) {
    temp = longStart;
    longStart = longEnd;
    longEnd = temp;
  }

  // keep the values bounded on touch screens
  if (latStart < 0)
    latStart = 0;
  if (longStart < 0)
    longStart = 0;
  if (latEnd > canvas.height)
    latEnd = canvas.height;
  if (longEnd > canvas.width)
    longEnd = canvas.width;

  latStartRatio.value = latStart / canvas.height;
  latEndRatio.value = latEnd / canvas.height;
  longStartRatio.value = longStart / canvas.width;
  longEndRatio.value = longEnd / canvas.width;
}

function mouseDown(e) {
  rect.startX = e.pageX - this.offsetLeft;
  rect.startY = e.pageY - this.offsetTop;
  drag = true;
}

function mouseUp() {
  drag = false;
}

// Draw a rectangular region as the mouse/finger moves
function mouseMove(e) {
  if (drag) {
    rect.w = (e.pageX - this.offsetLeft) - rect.startX;
    rect.h = (e.pageY - this.offsetTop) - rect.startY;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    draw();
  }
}

// Set up touch events
canvas.addEventListener("touchstart", function (e) {
  mousePos = getTouchPos(canvas, e);
  var touch = e.touches[0];
  var mouseEvent = new MouseEvent("mousedown", {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  canvas.dispatchEvent(mouseEvent);
}, false);
canvas.addEventListener("touchend", function (e) {
  var mouseEvent = new MouseEvent("mouseup", {});
  canvas.dispatchEvent(mouseEvent);
}, false);
canvas.addEventListener("touchmove", function (e) {
  var touch = e.touches[0];
  var mouseEvent = new MouseEvent("mousemove", {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  canvas.dispatchEvent(mouseEvent);
}, false);

// Get the position of a touch relative to the canvas
function getTouchPos(canvasDom, touchEvent) {
  var rect = canvasDom.getBoundingClientRect();
  return {
    x: touchEvent.touches[0].clientX - rect.left,
    y: touchEvent.touches[0].clientY - rect.top
  };
}

// Prevent scrolling when touching the canvas
document.body.addEventListener("touchstart", function (e) {
  if (e.target == canvas) {
    e.preventDefault();
  }
}, false);
document.body.addEventListener("touchend", function (e) {
  if (e.target == canvas) {
    e.preventDefault();
  }
}, false);
document.body.addEventListener("touchmove", function (e) {
  if (e.target == canvas) {
    e.preventDefault();
  }
}, false);
