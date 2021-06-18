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

// var svg = document.querySelector("svg");

const GAME_WIDTH = 600;
const GAME_HEIGHT = 600;
const SCORE_WIDTH = 300;
const SCORE_HEIGHT = 600;
const CELL_SIZE = GAME_WIDTH / 10;

window.canvas.width = GAME_WIDTH;
window.canvas.height = GAME_HEIGHT;

window.canvas.style.top = "5%"
window.canvas.style.left = "25%";
window.canvas.style.position = "absolute";

scoreDisp.style.left = "70%";
scoreDisp.style.top = "5%";
scoreDisp.style.position = "absolute";

//set SVG (for curves as an element of the canvas)

window.spawnPoints = [];
window.boardNames = [];

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

const spawnPoint3 = { x: 0, y: 8 };
window.spawnPoints.push(spawnPoint3);
window.spawnPoints.push(spawnPoint3);

const boardName3 = "player_board_2";
window.boardNames.push(boardName3);
window.boardNames.push(boardName3);

const spawnPoint4 = { x: 8, y: 8 };
window.spawnPoints.push(spawnPoint4);
window.spawnPoints.push(spawnPoint4);

const boardName4 = "player_board_3";
window.boardNames.push(boardName4);
window.boardNames.push(boardName4);

const spawnPoint5 = { x: 0, y: 7 };
window.spawnPoints.push(spawnPoint5);
window.spawnPoints.push(spawnPoint5);

const boardName5 = "player_board_4";
window.boardNames.push(boardName5);
window.boardNames.push(boardName5);

//------------------------------------------------
window.game = null;
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

//creates button
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
var nextRect = {
  x: 500,
  y: 550,
  width: 100,
  height: 50
};

let offset = 450;

var leftRect = {
  x: 215+8+offset-65,
  y: 530-200,
  width: 70,
  height: 50
};

var rightRect = {
  x: 315-8+offset-65,
  y: 530-200,
  width: 70,
  height: 50
};

var sameRect = {
  x: 155+8+offset-65,
  y: 590-200,
  width: 130,
  height: 50
};

var incRect = {
  x: 315-8+offset-65,
  y: 590-200,
  width: 130,
  height: 50
};

//Binding the click event on the canvas
window.canvas.addEventListener(
  "click",
  function (evt) {
    let mousePos = getMousePos(window.canvas, evt);

    if (isInside(mousePos, nextRect) && !this.finishedIns) {
      window.im.insScene += 1;
    } else if (isInside(mousePos,leftRect) && window.begunQueries) {
      window.qm.pressed = true;
      window.qm.queried("left");
    } else if (isInside(mousePos,rightRect) && window.begunQueries) {
      window.qm.pressed = true;
      window.qm.queried("right");
    }else if (isInside(mousePos,sameRect) && window.begunQueries) {
      window.qm.pressed = true;
      window.qm.queried("same");
    }else if (isInside(mousePos,incRect) && window.begunQueries) {
      window.qm.pressed = true;
      window.qm.queried("dis");
    }
  },
  false
);

//------------------------------------------------

function startNewGame() {
  if (
    window.finished_game &&
    window.timestep < window.total_tsteps &&
    window.n_games < window.max_games
  ) {
    window.finished_game = false;

    let boardName;
    let spawnPoint;
    if (window.disTraj) {
      boardName = "test_single_goal";
      spawnPoint = { x: 0, y: 0 };
    } else {
      boardName = window.boardNames[window.n_games];
      spawnPoint = window.spawnPoints[window.n_games];
    }

    window.game = new Game(
      GAME_WIDTH,
      GAME_HEIGHT,
      spawnPoint,
      boardName,
      window.disTraj
    );
    window.game.start();
    window.score = new Score(window.game);
    window.score.start();

    window.lastTime = 0;
    window.alpha = 1; /// current alpha value
    window.delta = 0.005; /// delta = speed
    window.n_games += 1;
    window.begunQueries = false;
    ctx.globalAlpha = 1;

    if (window.n_games === window.max_games) window.n_games = 0;
  }
}

function gameLoop(timestamp) {
  ctx.clearRect(0, 0, GAME_WIDTH, GAME_HEIGHT);
  ctxScore.clearRect(0, 0, SCORE_WIDTH, SCORE_HEIGHT);
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
    window.qm.draw(ctx);
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

        if (window.timestep > window.total_tsteps) {
          window.game.reached_terminal = true;
          window.im.finishedIns = false;
          window.im.finishedGamePlay = true;
        }
      }
    } else {
      window.finished_game = true;
    }
    requestAnimationFrame(gameLoop);
  }
}

requestAnimationFrame(gameLoop);
