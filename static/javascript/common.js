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
};

function change_attribute(username, attr_name, new_value) {
  start_firebase();
  firebase.database().ref("users").once("value").then(function(snapshot) {
    var users = snapshot.val();
    var user_id = -1;
    for (var i = 0; i < users.length; i++) {
      if (users[i]["name"] == username) {
        user_id = i;
      }
    };
    firebase.database().ref("users/"+ user_id.toString() + "/").update(
      {attr_name: new_value});
  });
};

function get_attribute(username, attr_name) {
  var attr_val = "";
  start_firebase();
  firebase.database().ref("users").once("value").then(function(snapshot) {
    var users = snapshot.val();
    var user_id = -1;
    for (var i = 0; i < users.length; i++) {
      if (users[i]["name"] == username) {
        user_id = i;
        attr_val = users[i][attr_name];
      }
    };
  });
  return attr_val;
};

function increment_question(username) {
  start_firebase();
  firebase.database().ref("users").once("value").then(function(snapshot) {
    var cur_qid = 0;
    var users = snapshot.val();
    var user_id = -1;
    for (var i = 0; i < users.length; i++) {
      if (users[i]["name"] == username) {
        user_id = i;
        cur_qid = users[i]["trivia_question"];
      }
    };
    firebase.database().ref("users/"+ user_id.toString() + "/").update(
      {"trivia_question": cur_qid + 1});
  });
};

function post_score(gameid, username, score) {
  start_firebase();
  firebase.database().ref("users").once("value").then(function(snapshot) {
    var curr_game_score = 0;
    var curr_total_score = 0;
    gameid += "_score";
    var users = snapshot.val();
    var user_id = -1;
    for (var i = 0; i < users.length; i++) {
      if (users[i]["name"] == username) {
        user_id = i;
        curr_game_score = users[i][gameid];
        curr_total_score = users[i]["score"];
      }
    };
    var updateObj = {};
    updateObj[gameid] = Math.max(curr_game_score, score);
    updateObj[score] = curr_total_score + Math.max(Math.max(curr_game_score, score) - 
      Math.min(curr_game_score, score), 0)
    if (user_id != -1) {
      firebase.database().ref("users/"+ user_id.toString() + "/").update(updateObj);
    }
  });
}

function increase_score(gameid, user_id, score) {
  start_firebase();
  firebase.database().ref("users").once("value").then(function(snapshot) {
    gameid += "_score";
    var users = snapshot.val();
    var curr_game_score = users[user_id][gameid];
    var curr_total_score = users[user_id]["score"];
    var updateObj = {};
    updateObj[gameid] = curr_game_score + score;
    updateObj["score"] = curr_total_score + score;

    firebase.database().ref("users/"+ user_id.toString() + "/").update(
      updateObj);

  });
}