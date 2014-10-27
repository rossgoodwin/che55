import ddf.minim.*;

Minim minim1;
Minim minim2;
Minim minim3;
Minim minim4;
AudioPlayer player1;
AudioPlayer player2;
AudioPlayer player3;
AudioPlayer player4;

int score = 0;
boolean[] status = new boolean[11];
String[] tracks = {"n.mp3", "w1.mp3", "w2.mp3", "w3.mp3", "b1.mp3", "b2.mp3", "b3.mp3"};

void allStatusTrue() {
  for (int i=0; i<11; i++) {
    status[i] = true;
  }
}

void playTracks(int s, int t1, int t2, int t3, int t4) {
  allStatusTrue();
  status[s] = false;
  
  player1.close();
  player2.close();
  player3.close();
  player4.close();
  player1 = minim1.loadFile(tracks[t1]);
  player2 = minim2.loadFile(tracks[t2]);
  player3 = minim3.loadFile(tracks[t3]);
  player4 = minim4.loadFile(tracks[t4]);
  player1.loop();
  player2.loop();
  player3.loop();
  player4.loop();
  
  print(s);
  print(":");
  print(" "+tracks[t1]+",");
  print(tracks[t2]+",");
  print(tracks[t3]+",");
  println(tracks[t4]);
}

void setup() {
  minim1 = new Minim(this);
  minim2 = new Minim(this);
  minim3 = new Minim(this);
  minim4 = new Minim(this);
  
  allStatusTrue();
  
  player1 = minim1.loadFile("n.mp3");
  player2 = minim2.loadFile("n.mp3");
  player3 = minim3.loadFile("n.mp3");
  player4 = minim4.loadFile("n.mp3");
  player1.loop();
  player2.loop();
  player3.loop();
  player4.loop();
}

void draw() {
  String scoreString[] = loadStrings("score.txt");
  score = int(scoreString[0]);
  //println(score);
  
  // status 0: score <= -450
  if (score <= -450 && status[0]) {
    playTracks(0, 4, 5, 6, 0);
  }
  // status 1: -350 >= score > -450
  else if (score <= -350 && score > -450 && status[1]) {
    playTracks(1, 4, 5, 0, 0);
  }
  // status 2: -250 >= score > -350
  else if (score <= -250 && score > -350 && status[2]) {
    playTracks(2, 4, 0, 0, 0);
  }
  // status 3: -150 >= score > -250
  else if (score <= -150 && score > -250 && status[3]) {
    playTracks(3, 1, 4, 5, 6);
  }
  // status 4: -50 >= score > -150
  else if (score <= -50 && score > -150 && status[4]) {
    playTracks(4, 1, 4, 5, 0);
  }
  // status 5: -50 < score < 50
  else if (abs(score) < 50 && status[5]) {
    playTracks(5, 1, 4, 0, 0); //<>//
  }
  // status 6: 50 <= score < 150
  else if (score >= 50 && score < 150 && status[6]) {
    playTracks(6, 1, 2, 4, 0);
  }
  // status 7: 150 <= score < 250
  else if (score >= 150 && score < 250 && status[7]) {
    playTracks(7, 1, 2, 3, 4);
  }
  // status 8: 250 <= score < 350
  else if (score >= 250 && score < 350 && status[8]) {
    playTracks(8, 1, 0, 0, 0);
  }
  // status 9: 350 <= score < 450
  else if (score >= 350 && score < 450 && status[9]) {
    playTracks(9, 1, 2, 0, 0);
  }
  // status 10: score >= 450
  else if (score >= 450 && status[10]) {
    playTracks(10, 1, 2, 3, 0);
  }
}
