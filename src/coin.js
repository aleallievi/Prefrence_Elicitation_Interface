import { detectCollision } from "./collisionDetection";

export default class Coin {
  constructor(game, position) {
    this.img = document.getElementById("img_coin");

    this.game = game;

    this.position = position;
    this.size_x = 30;
    this.size_y = 30;
    this.cellSize = game.gameWidth / 10;
    this.lastCol = { x: -1, y: -1 };

    // this.markedForDeletion = false;
  }

  update() {
    if (detectCollision(this.game.vehicle, this)) {
      // this.game.ball.speed.y = -this.game.ball.speed.y;
      // this.markedForDeletion = true;
      this.game.find_is_leaving_ow(this.position);
      if (!this.game.isLeaving) {
        // this.game.score += 1;
        // this.game.pScore += 1;
        this.game.collectedCoin = true;
        this.game.vehicle.updatedScore = true;
      }
    }
  }

  draw(ctx) {
    // console.log(this.position);
    ctx.drawImage(
      this.img,
      this.cellSize * this.position.x + this.cellSize / 2 - this.size_x / 2,
      this.cellSize * this.position.y + this.cellSize / 2 - this.size_y / 2,
      this.size_x,
      this.size_y
    );
  }
}
