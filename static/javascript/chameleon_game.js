var score = 0;

function change_color(div_id, div_id2) {
	// Function changes the Octocat color/position and game background and updates score whenever the Octocat is clicked
    document.getElementById("confirm-submit").innerHTML = "Never mind...";
	rando = Math.random() * 100;
    document.getElementById(div_id).style.backgroundColor = get_BGcolor(rando);
	document.getElementsByClassName(div_id2)[1].style.color = get_OCcolor(rando);
	document.getElementsByClassName(div_id2)[1].style.position = "relative";
	document.getElementsByClassName(div_id2)[1].style.top = random_percent_top();
	document.getElementsByClassName(div_id2)[1].style.left = random_percent_left();
    score++;
	document.getElementById('scores').innerHTML = 'Your Current Score: ' + score.toString();
}

function get_BGcolor(rando){
	//  Uses input argument (random int between 0 - 100) to choose a corresponding background color. 
	if (rando <= 5)
		return '#18b495';
	else if (rando <= 10)
		return '#159d82';
	else if (rando <= 15)
		return '#2fd072';
	else if (rando <= 20)
		return '#26a65b';
	else if (rando <= 25)
		return '#3c9cdd';
	else if (rando <= 30)
		return '#2981bc';
	else if (rando <= 35)
		return '#a05fb9';
	else if (rando <= 40)
		return '#9243ad';
	else if (rando <= 45)
		return '#364d63';
	else if (rando <= 50)
		return '#2d4052';
	else if (rando <= 55)
		return '#ecc113';
	else if (rando <= 60)
		return '#ec9b18';
	else if (rando <= 65)
		return '#e67919';
	else if (rando <= 70)
		return '#cc5200';
	else if (rando <= 75)
		return '#e64533';
	else if (rando <= 80)
		return '#bb392a';
	else if (rando <= 85)
		return '#f0f3f4';
	else if (rando <= 90)
		return '#bac0c4';
	else if (rando <= 95)
		return '#90a1a2';
	else if (rando <= 100)
		return '#80878e';
}

function get_OCcolor(rando){
	//  Uses input argument (random int between 0 - 100) to choose a corresponding Octocat color. 
	if (rando <= 5)
		return '#1abc9c';
	else if (rando <= 10)
		return '#1abc9c';
	else if (rando <= 15)
		return '#2ECC71';
	else if (rando <= 20)
		return '#27AE60';
	else if (rando <= 25)
		return '#3498DB';
	else if (rando <= 30)
		return '#2980B9';
	else if (rando <= 35)
		return '#9B59B6';
	else if (rando <= 40)
		return '#8E44AD';
	else if (rando <= 45)
		return '#34495E';
	else if (rando <= 50)
		return '#2C3E50';
	else if (rando <= 55)
		return '#F1C40F';
	else if (rando <= 60)
		return '#F39C12';
	else if (rando <= 65)
		return '#E67E22';
	else if (rando <= 70)
		return '#D35400';
	else if (rando <= 75)
		return '#E74C3C';
	else if (rando <= 80)
		return '#C0392B';
	else if (rando <= 85)
		return '#ECF0F1';
	else if (rando <= 90)
		return '#BDC3C7';
	else if (rando <= 95)
		return '#95A5A6';
	else if (rando <= 100)
		return '#7F8C8D';
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