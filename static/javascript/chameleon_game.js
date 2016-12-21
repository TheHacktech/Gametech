// Variables
var score = 0;
var BC_colors = ['#18b495','#159d82', '#2fd072', '#26a65b', '#3c9cdd', '#2981bc', '#a05fb9', '#9243ad', '#364d63', '#2d4052', '#ecc113', '#ec9b18', '#e67919', '#cc5200', '#e64533', '#bb392a', '#f0f3f4', '#bac0c4', '#90a1a2', '#80878e'];
var OC_colors = ['#1abc9c','#16A085', '#2ECC71', '#27AE60', '#3498DB', '#2980B9', '#9B59B6', '#8E44AD', '#34495E', '#2C3E50', '#F1C40F', '#F39C12', '#E67E22', '#D35400', '#E74C3C', '#C0392B', '#ECF0F1', '#BDC3C7', '#95A5A6', '#7F8C8D'];

function change_color(div_id, div_id2) {
	// Function changes the Octocat color/position and game background and updates score whenever the Octocat is clicked
    document.getElementById("confirm-submit").innerHTML = "Never mind...";
	rando = Math.floor(Math.random() * 100) % 20;
    document.getElementById(div_id).style.backgroundColor = BC_colors[rando];
	document.getElementsByClassName(div_id2)[1].style.color = OC_colors[rando];
	document.getElementsByClassName(div_id2)[1].style.position = "relative";
	document.getElementsByClassName(div_id2)[1].style.top = random_percent_top();
	document.getElementsByClassName(div_id2)[1].style.left = random_percent_left();
    score++;
	document.getElementById('scores').innerHTML = 'Your Current Score: ' + score.toString();
}

function random_percent_left(){
   //  Randomly generates a position as a string % to representing the horizontal position of Octocat (between -64% and 64%)
   rando = Math.random() * 64;
   rando2 = Math.random();
   if (rando2 < 0.5){
	rando = rando * -1;
   }
   return rando.toString() + '%';
}

function random_percent_top(){
   //  Randomly generates a position as a string % to representing the vertical position of Octocat (between -31% and 115%)
   rando = Math.random() * 71;
   rando2 = Math.random();
   if (rando2 < 0.5){
	rando = rando * -1;
   }
   rando = rando + 42;
   return rando.toString() + '%';
}