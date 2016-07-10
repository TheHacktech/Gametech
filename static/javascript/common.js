var firebase_started = false;
var config = {
  apiKey: "AIzaSyDq5GXyq96eg0FsUOfVM4XhH1cBS57m4C8",
  authDomain: "minigames-15a0f.firebaseapp.com",
  databaseURL: "https://minigames-15a0f.firebaseio.com",
  storageBucket: "minigames-15a0f.appspot.com",
};

function start_firebase() {
  if (!firebase_started) {
    firebase.initializeApp(config);
    firebase_started = true;
  }
}

function post_score(gameid, username, score) {
  start_firebase();
  firebase.database().ref("users").once("value").then(function(snapshot) {
    var curr_score = 0;
    var users = snapshot.val();
    var user_id = -1;
    for (var i = 0; i < users.length; i++) {
      if (users[i]["name"] == username) {
        user_id = i;
        curr_score = users[i]["score"];
      }
    }
    firebase.database().ref("users/"+ user_id.toString() + "/").update(
      {"score": curr_score + score});

  });
}
