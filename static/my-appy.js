var drawingApp = (function () {
	"use strict";

	var canvas,
		context,
		canvasWidth = window.innerWidth,
		canvasHeight = window.innerHeight-200,
		clickX = [],
		clickY = [],
		colorPurple = "#cb3594",
		colorGreen = "#659b41",
		colorYellow = "#ffcf33",
		colorBrown = "#986928",
		colorBlack = "#000000",
		x = canvasWidth/2,
		y = canvasHeight/2,
		len = 50,
	// clears the canvas.
	clearCanvas = function () {
		context.clearRect(0, 0, canvasWidth, canvasHeight);
	},
	mainDraw = function(newX, newY, color){
		context.beginPath();
		context.moveTo(x, y);
		context.lineTo(newX, newY);
		x = newX;
		y = newY;
		context.lineWidth = 5;
		context.lineCap = 'square';
		if( !color){
			context.strokeStyle = colorBlack;
		} else {
			context.strokeStyle = color;
		}
		context.stroke();
		context.closePath();
	},
	up = function (color){
		var newY = y-len;
		if(newY < 0){
			mainDraw(x, 0, color);
			y = canvasHeight;
			mainDraw(x, canvasHeight-Math.abs(newY), color);
		} else {
			mainDraw(x, newY, color);		
		}
	},
	down = function (color){
		var newY = y+len;
		if(newY > canvasHeight){
			mainDraw(x, canvasHeight, color);
			y = 0;
			mainDraw(x, newY - canvasHeight, color);
		} else {
			mainDraw(x, newY, color);
		}
	},
	left = function (color){
		var newX = x-len;
		if(newX<0){
			mainDraw(0, y,color);
			x = canvasWidth;
			mainDraw(canvasWidth-Math.abs(newX), y,color);
		} else {
			mainDraw(newX, y, color);
		}

	},
	right = function (color){
		var newX = x+len;
		if(newX>canvasWidth){
			mainDraw(canvasWidth, y, color);
			x = 0;
			mainDraw(newX-canvasWidth, y, color);
		} else {
			mainDraw(newX, y, color);
		}
	},
	init = function() {
		canvas = document.createElement('canvas');
		canvas.setAttribute('width', canvasWidth);
		canvas.setAttribute('height', canvasHeight);
		canvas.setAttribute('id', 'canvas');

		document.getElementById('canvasDiv').appendChild(canvas);
		if (typeof G_vmlCanvasManager !== "undefined") {
			canvas = G_vmlCanvasManager.initElement(canvas);
		}
		context = canvas.getContext("2d"); 

		var namespace = '/test';
	    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
	    socket.on('my response', function(msg) {
	        $('#log').append('<br>' + $('<div/>').text('Received #' + msg.direction + ': ' + msg.color).html());
	        var color = msg.color;
	        if(!color){
	        	color = 'black';
	        }
	        if(msg.direction === 'up'){
	        	up(color);
	        } else if(msg.direction === 'down') {
	        	down(color);
	        } else if(msg.direction === 'left') {
	        	left(color);
	        } else if(msg.direction ==='right') {
	        	right(color);
	        }
	    });
	};
	return {
		init: init
	};
}());