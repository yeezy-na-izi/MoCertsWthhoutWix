
 window.addEventListener('DOMContentLoaded', function()  {
    
    'use strict'

    var menu = document.querySelector('.menu-wrap'),
    menuItem = document.querySelectorAll('.menu-link'),
    hamburger = document.querySelector('.header__hamburger');
    console.log (menu);
    console.log (menuItem);
    console.log (hamburger);

    hamburger.addEventListener('click', function()  {
    hamburger.classList.toggle('hamburger_active');
    menu.classList.toggle('top_active');

    });

    for (var i=0; i < menuItem.length; i++) {
      var element = menuItem[i];
      console.log (element);
        element.addEventListener('click', function(){
        hamburger.classList.toggle('hamburger_active');
        menu.classList.toggle('top_active');
      });
    };

    $('.EN').click(function(){
        $('.select-list').toggle();
        $('.arrow').toggleClass('rotate');

    })


});

// snake mouse

var width, height
var step = 0;
var canvas = document.createElement('canvas')
var ctx = canvas.getContext('2d')
var bg = [255, 255, 255]

// mouse coordinates
function Mouse () {
  this.x = window.innerWidth / 2
  this.y = window.innerHeight / 2
}
var mouse = new Mouse()
document.onmousemove = function(e){ mouse.x = e.clientX; mouse.y = e.clientY}

document.getElementsByTagName('body')[0].appendChild(canvas)
canvas.style="position:fixed; top:0; left:0; pointer-events: none;"
window.addEventListener('resize', setup);
setup();

function setup() {
  canvas.width = width = window.innerWidth;
  canvas.height = height = window.innerHeight;
}

window.requestAnimationFrame(animate);

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  draw();

  step++;
  window.requestAnimationFrame(function(){animate()});
}

function Flwr () {
  this.follow = null
  this.child = null
  this.x = mouse.x
  this.y = mouse.y
  this.dx = 0
  this.dy = 0
  this.a = 0.35
  this.b = 0.54
  this.n = 0
}

var flwr, flwrPrev, train = [], i, n = 50;
for (i = 0; i < n; i++) {
  flwr = new Flwr()
  flwr.n = i
  if (flwrPrev) {
    flwr.b = flwrPrev.b + (0.1/n)
    flwr.follow = flwrPrev
    flwrPrev.child = flwr
  } else {
    flwr.follow = mouse
  }
  flwrPrev = flwr
  train.push(flwr)
}

function draw () {
  for (i in train) {
    // update position
    flwr = train[i]
    var dx = flwr.follow.x - flwr.x
    var dy = flwr.follow.y - flwr.y

    flwr.dx = flwr.dx * flwr.a + dx * (1 - flwr.a)
    flwr.dy = flwr.dy * flwr.a + dy * (1 - flwr.a)

    flwr.x = flwr.dx * flwr.b + flwr.x
    flwr.y = flwr.dy * flwr.b + flwr.y


    if (flwr.follow !== mouse) {
      ctx.beginPath();
      ctx.strokeStyle = '#5b1f43'
      ctx.lineCap = 'round'
      ctx.lineWidth = (n-flwr.n)/n * 1 + 2 // 8 + 2 чем меньше тем змейка короче
      ctx.moveTo(flwr.x,flwr.y);
      ctx.lineTo(flwr.follow.x,flwr.follow.y);
      ctx.stroke();
    }
  }
}

function drawCircle (context, x, y, r) {
  context.arc(x ,y , r, 0, 2*Math.PI);
}

function fillCanvas (context, color, alpha) {
  context.rect(0, 0, this.width, this.height)
  context.fillStyle = `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${alpha})`
  context.fill()
}

// Сенсорный скролинг