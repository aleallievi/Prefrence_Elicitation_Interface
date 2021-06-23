import 'regenerator-runtime/runtime'
// import regeneratorRuntime from "regenerator-runtime";

import Game from "/src/game";
import Score from "/src/score";
import InstructionsManager from "/src/instructionsManager";
import QueryManager from "/src/queryManager"
//---------------------------------MTURK STUFF--------------------------------------
// var AWS = require('aws-sdk');
// var region_name = 'us-east-1';
// var endpoint = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com';
// // Uncomment this line to use in production
// //var endpoint = 'https://mturk-requester.us-east-1.amazonaws.com';
// AWS.config.update({ region: 'us-east-1',
// 		    endpoint: endpoint });
//
// var mturk = new AWS.MTurk();
// //
// let QUESTION_XML = '<ExternalQuestion' +
//  'xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">' +
//  '<ExternalURL>"https://dev.d1e16e31dm86sr.amplifyapp.com"</ExternalURL>' +
//  '<FrameHeight>500</FrameHeight>' + '</ExternalQuestion>'
//

//---------------------------------MTURK STUFF--------------------------------------

window.canvas = document.getElementById("gameScreen");
let ctx = window.canvas.getContext("2d");

let scoreDisp = document.getElementById("scoreScreen");
let ctxScore = scoreDisp.getContext("2d");

let queryDisp = document.getElementById("queryScreen");
let ctxQuery = queryDisp.getContext("2d");

// var svg = document.querySelector("svg");

const GAME_WIDTH = 600;
const GAME_HEIGHT = 600;
const QUERY_WIDTH = 1200;
const QUERY_HEIGHT = 700;
const SCORE_WIDTH = 300;
const SCORE_HEIGHT = 600;
//width="300" height="600"
const CELL_SIZE = GAME_WIDTH / 10;
//
//
// console.log(window.innerWidth);
// console.log(window.innerHeight);
//
// window.canvas.width = GAME_WIDTH;
// window.canvas.height = GAME_HEIGHT;

window.gsWidth = window.canvas.width;
window.gsHeight = window.canvas.height;

window.qdWidth = 0.8*$(window).width();
window.qdHeight= 0.8*$(window).height();


window.canvas.width = 0.416*window.innerWidth
window.canvas.height = 0.416*window.innerWidth


window.canvas.style.left = "29.1%";
window.canvas.style.top = "5%"
window.canvas.style.position = "absolute";
//
// scoreDisp.width = 300;
// scoreDisp.height = 600;
scoreDisp.width = 0.208*window.innerWidth;
scoreDisp.height = 0.858*window.innerHeight;

scoreDisp.style.left = "75%";
scoreDisp.style.top = "5%";
scoreDisp.style.position = "absolute";

// queryDisp.width = QUERY_WIDTH;
// queryDisp.height = QUERY_HEIGHT;
queryDisp.width = 0.8*window.innerWidth;
queryDisp.height = 0.8*window.innerHeight;

queryDisp.style.left = "7%";
queryDisp.style.top = "5%";
queryDisp.style.position = "absolute";


window.addEventListener("resize", function(event) {
  // let dw = window.innerWidth/window.canvas.width;
  // let hw = window.innerHeight/window.canvas.height;
  // console.log(dw);
  // console.log(hw);
  // ctx.scale(dw, hw);
  var gs = $('#gameScreen');
  gs.css("width", 0.416*$(window).width());
  gs.css("height", 0.416*$(window).width());

  var sd = $('#scoreScreen');
  sd.css("width", 0.208*$(window).width());
  sd.css("height",0.858*$(window).height());

  var qs = $('#queryScreen');
  qs.css("width", 0.8*$(window).width());
  qs.css("height",0.8*$(window).height());


  window.gsWidth = 0.416*$(window).width();
  window.gsHeight = 0.416*$(window).height();

  window.qdWidth = 0.8*$(window).width();
  window.qdHeight= 0.8*$(window).height();

  rects = updateRects(window.gsWidth, window.gsWidth);


  window.nextRect = rects[0];
  window.leftRect = rects[1];
  window.rightRect = rects[2];
  window.sameRect = rects[3];
  window.incRect = rects[4];


});

//set SVG (for curves as an element of the canvas)

window.spawnPoints = [];
window.boardNames = [];
window.instructions = [];

// const spawnPoint1 = { x: 0, y: 5 };
// window.spawnPoints.push(spawnPoint1);
// const boardName1 = "player_board_1";
// window.boardNames.push(boardName1);

const spawnPoint2 = { x: 0, y: 5 };
window.spawnPoints.push(spawnPoint2);
window.spawnPoints.push(spawnPoint2);

const boardName2 = "player_board_1";
window.boardNames.push(boardName2);
window.boardNames.push(boardName2);

window.instructions.push("https://raw.githubusercontent.com/Stephanehk/Prefrence_Elicitation_Interface/main/assets/images/board_1_ins.png");
window.instructions.push("https://raw.githubusercontent.com/Stephanehk/Prefrence_Elicitation_Interface/main/assets/images/board_1_ins.png");

const spawnPoint3 = { x: 0, y: 8 };
window.spawnPoints.push(spawnPoint3);
window.spawnPoints.push(spawnPoint3);

const boardName3 = "redone_player_board_2";
window.boardNames.push(boardName3);
window.boardNames.push(boardName3);

window.instructions.push("https://raw.githubusercontent.com/Stephanehk/Prefrence_Elicitation_Interface/main/assets/images/board_2_ins.png");
window.instructions.push("https://raw.githubusercontent.com/Stephanehk/Prefrence_Elicitation_Interface/main/assets/images/board_2_ins.png");


const spawnPoint4 = { x: 8, y: 9 };
window.spawnPoints.push(spawnPoint4);
window.spawnPoints.push(spawnPoint4);

const boardName4 = "redone_player_board_3";
window.boardNames.push(boardName4);
window.boardNames.push(boardName4);

window.instructions.push("https://raw.githubusercontent.com/Stephanehk/Prefrence_Elicitation_Interface/main/assets/images/board_3_ins.png");
window.instructions.push("https://raw.githubusercontent.com/Stephanehk/Prefrence_Elicitation_Interface/main/assets/images/board_3_ins.png");


const spawnPoint5 = { x: 0, y: 7 };
window.spawnPoints.push(spawnPoint5);
window.spawnPoints.push(spawnPoint5);

const boardName5 = "redone_player_board_4";
window.boardNames.push(boardName5);
window.boardNames.push(boardName5);

window.instructions.push("https://raw.githubusercontent.com/Stephanehk/Prefrence_Elicitation_Interface/main/assets/images/board_4_ins.png");
window.instructions.push("https://raw.githubusercontent.com/Stephanehk/Prefrence_Elicitation_Interface/main/assets/images/board_4_ins.png");

//------------------------------------------------
window.game = null;
window.playTrajBoard = false;
window.finishedTrajBoard = false;
window.n_games = 0;
window.max_games = 8;
window.finished_game = true;
window.total_tsteps = 2;
window.timestep = 0;
//NOTE: USE THIS LINK TO VIEW TRAJECTORIES https://codesandbox.io/s/gridworld-dwkdg?file=/src/trajHandler.js
window.disTraj = false;
window.im = new InstructionsManager();
window.qm = new QueryManager();
// window.im.createButton(canvas, ctx);

//creates buttons
window.rects = updateRects(window.canvas.width, window.canvas.height);
window.nextRect = rects[0];
window.leftRect = rects[1];
window.rightRect = rects[2];
window.sameRect = rects[3];
window.incRect = rects[4];
//------------------------------------------------
//https://stackoverflow.com/questions/24384368/simple-button-in-html5-canvas/24384882
function getMousePos(canvas, event) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  };
}

function isInside(pos, rect) {
  return (
    pos.x > rect.x &&
    pos.x < rect.x + rect.width &&
    pos.y < rect.y + rect.height &&
    pos.y > rect.y
  );
}


function updateRects(w,h) {

  var nextRect = {
    x: 0.833*w,
    y: 0.916*w,
    width: 100,
    height: 50
  };

  let offset = 0.434*window.qdWidth;
  var leftRect = {
    x: 0.238*window.qdWidth,
    y: 0.894*window.qdHeight,
    width: 50,
    height: 70
  };

  var rightRect = {
    x: (0.316*window.qdWidth)+offset,
    y: 0.894*window.qdHeight,
    width: 50,
    height: 70
  };

  var sameRect = {
    x: 0.468*window.qdWidth,
    y: 0.76*window.qdHeight,
    width: 130,
    height: 50
  };

  var incRect = {
    x:  0.468*window.qdWidth,
    y: 0.894*window.qdHeight,
    width: 130,
    height: 50
  };
  return [nextRect, leftRect, rightRect, sameRect, incRect]
}


//Binding the click event on the canvas
window.canvas.addEventListener(
  "click",
  function (evt) {
    let mousePos = getMousePos(window.canvas, evt);

    if (isInside(mousePos, window.nextRect) && !this.finishedIns) {
      window.im.insScene += 1;
    }
  },
  false
);

queryDisp.addEventListener(
  "click",
  function (evt) {
    let mousePos = getMousePos(queryDisp, evt);
    if (isInside(mousePos,window.leftRect) && window.begunQueries) {
      window.qm.pressed = true;
      window.qm.queried("left");
      console.log("left");
    } else if (isInside(mousePos,window.rightRect) && window.begunQueries) {
      window.qm.pressed = true;
      window.qm.queried("right");
      console.log("right");
    }else if (isInside(mousePos,window.sameRect) && window.begunQueries) {
      window.qm.pressed = true;
      window.qm.queried("same");
      console.log("same");
    }else if (isInside(mousePos,window.incRect) && window.begunQueries) {
      window.qm.pressed = true;
      window.qm.queried("dis");
      console.log("dis");
    }
  },
  false
);
//------------------------------------------------

function startNewGame() {
  if (window.finished_game && ((window.timestep < window.total_tsteps &&window.n_games < window.max_games) || window.playTrajBoard) ) {
    window.finished_game = false;

    let boardName;
    let spawnPoint;
    let ins = "";
    let dispIns = true;
    if (window.disTraj) {
      boardName = "test_single_goal_mud";
      spawnPoint = { x: 0, y: 0 };
    } else if (window.playTrajBoard) {
      boardName = "test_single_goal_mud";
      spawnPoint ={ x: 0, y: 0 };
      dispIns = false;
    } else {
      boardName = window.boardNames[window.n_games];
      spawnPoint = window.spawnPoints[window.n_games];
      ins = window.instructions[window.n_games];
    }

    // if (window.n_games===window.max_games) {
    //   //play the trajectory board
    // }

    window.game = new Game(
      GAME_WIDTH,
      GAME_HEIGHT,
      spawnPoint,
      boardName,
      window.disTraj
    );
    window.game.start(ins=ins,dispIns=dispIns);
    window.score = new Score(window.game);
    window.score.start();

    window.lastTime = 0;
    window.alpha = 1; /// current alpha value
    window.delta = 0.005; /// delta = speed
    window.n_games += 1;
    window.begunQueries = false;
    ctx.globalAlpha = 1;

    // if (window.n_games === window.max_games) {
    //   return;
    // }
  }
}

function gameLoop(timestamp) {
  ctx.clearRect(0, 0, window.canvas.width, window.canvas.height);
  ctxScore.clearRect(0, 0, scoreDisp.width, scoreDisp.height);
  ctxQuery.clearRect(0,0,queryDisp.width,queryDisp.height);
  let deltaTime = timestamp - window.lastTime;

  if (!window.im.finishedIns && !window.disTraj) {
    ctx.globalAlpha = 1;
    window.im.update();
    window.im.draw(ctx);
    requestAnimationFrame(gameLoop);
    // requestAnimationFrame(gameLoop);
  } else if (window.begunQueries) {
    ctx.globalAlpha = 1;
    window.qm.update(deltaTime);
    window.qm.draw(ctxQuery);

    requestAnimationFrame(gameLoop);

  }else {
    startNewGame();
    window.lastTime = timestamp;

    if (window.game.reached_terminal === true && !window.disTraj) {
      //figure out how to fade
      window.alpha -= window.delta;
      // if (alpha <= 0 || alpha >= 1) delta = -delta;
      ctx.globalAlpha = window.alpha;
      //clear a bunch of stuff like incompleteCords here
      //if user was playing game
    }

    if (window.alpha > 0) {
      if (window.game.gameObjects != null) {
        window.game.update(deltaTime);
        window.game.draw(ctx);
        window.score.update(deltaTime);
        window.score.draw(ctxScore);

        if (!window.playTrajBoard && (window.timestep > window.total_tsteps || window.n_games >= window.max_games)) {
          window.game.reached_terminal = true;
          window.im.finishedIns = false;
          window.im.finishedGamePlay = true;
          window.finished_game = true;
        }
      }
    } else {
      window.finished_game = true;
      if (window.playTrajBoard){
        window.playTrajBoard = false;
        window.im.finishedIns = false;
        window.im.finishedGamePlay = true;
        window.finishedTrajBoard = true;
      }
      // window.playTrajBoard = false;
    }
    requestAnimationFrame(gameLoop);
  }
}

requestAnimationFrame(gameLoop);
