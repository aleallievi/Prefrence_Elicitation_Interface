export default class Score {
  constructor(game, scoreWidth) {
    this.game = game;
  }
  start() {
    this.score = 0;
    this.prevScore = 0;
    this.prevprevScore = 0;
    this.lastx = 0;
    this.lasty = 0;
    this.lastw = 0;
    this.lasth = 0;
    this.startY = 300;
    this.decomposedScore = false;
    this.printDecomposed = true;
    this.gasScore = 0;
    this.prevGasScore = 0;
    this.pScore = 0;
    this.prevPScore = 0;
    this.maxHeight = 500;
    this.updateAll = false;
  }

  drawRect(ctx, x, y, w, h, color) {
    if (color === "white")console.log("printing white rect!!");
    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
    ctx.stroke();
  }

  barText(ctx, val, y_offset, text = "", fontSize = "20px") {
    ctx.font = fontSize + " CustomFont";
    let symbol = "$";
    if (val > 0) {
      ctx.fillStyle = "green";
      symbol = "+ $";
    }
    if (val < 0) {
      ctx.fillStyle = "red";
      symbol = "- $";
      val = -val;
    }
    if (val === 0) ctx.fillStyle = "brown";
    if (this.lasty > 20)
      ctx.fillText(
        text + symbol + String(val),
        220,
        this.cap(this.lasty + y_offset)
      );
    else
      ctx.fillText(
        text + symbol + String(val),
        220,
        this.cap(this.startY + 10 + y_offset)
      );
  }

  barImg(ctx, id, y_offset, x = 180, size = 30) {
    let img = document.getElementById(id);

    if (this.lasty > 20)
      ctx.drawImage(img, x, this.cap(this.lasty + y_offset), size, size);
    else
      ctx.drawImage(img, x, this.cap(this.startY + 10 + y_offset), size, size);
  }

  drawGasTank(ctx, x) {
    if (this.decomposedScore === false) return;
    let y = this.maxHeight;
    let w = 120;
    let h = -5 * 100;
    this.drawRect(ctx, x, y, w, h, "darkolivegreen");

    y = y - 5 * 100;
    h = -5 * this.gasScore;
    this.drawRect(ctx, x, y, w, h, "grey");

    ctx.font = "20px CustomFont";
    ctx.fillStyle = "black";
    // console.log("here");
    ctx.fillText(
      "Gas: $" + String(this.gasScore),
      x + 10,
      550 + 10 - 5 * this.gasScore - 450
    );
  }

  cap(y) {
    // return y;
    if (y > 500 || this.updateAll) {
      this.updateAll = true;
      let out = y - 500;

      // console.log(y);
      // console.log(500 + (y - 500));
      // console.log("\n");
      return 400 + out;
    }
    return y;
    // let max = 300;
    // if (Math.abs(val) + y > max) {
    //   if (val < 0) {
    //     val = -(max - y);
    //   } else {
    //     val = max - y;
    //   }
    // }
  }

  drawRects(ctx, x, w) {
    if (this.prevScore < 0) {
      // console.log(this.score);
      // console.log(this.prevscore);
      let py = this.startY - 5 * this.prevScore + 3;

      let ph = 5 * this.prevScore;
      this.drawRect(ctx, x, py, w, ph, "brown");

      if (this.delta < 0) {
        let y = py - 5 * (this.score - this.prevScore);
        let h = 5 * this.delta;
        this.drawRect(ctx, x, y, w, h, "red");

        this.lastx = x;
        this.lasty = y.valueOf();
        this.lastw = w;
        this.lasth = h.valueOf();
        this.color2draw = "red";
        // this.subtracter = 0;
        // this.step = 0;
      } else if (this.delta > 0) {
        let y;
        let h;
        if (this.score > 0) {
          //jump over the bar
          y = this.startY;
          h = -5 * (this.delta - this.prevScore);
          ctx.clearRect(x, py, w, ph);
        } else {
          y = this.startY - 5 * this.prevScore + 3;
          h = -5 * this.delta;
        }
        this.drawRect(ctx, x, y, w, h, "green");

        this.lastx = x;
        this.lasty = y.valueOf();
        this.lastw = w;
        this.lasth = h.valueOf();
        this.color2draw = "green";
      }
    }

    if (this.prevScore > 0) {
      let ph = -5 * this.prevScore;
      this.drawRect(ctx, x, this.startY, w, ph, "brown");

      if (this.delta > 0) {
        let y = this.startY + -5 * this.prevScore;
        let h = -5 * this.delta;
        this.drawRect(ctx, x, y, w, h, "green");
        // console.log(h);
        // console.log(y);

        this.lastx = x;
        this.lasty = y.valueOf();
        this.lastw = 120;
        this.lasth = h.valueOf();
        this.color2draw = "green";
      }
      if (this.delta < 0) {
        let y;
        let h;
        if (this.score < 0) {
          y = this.startY + 3;
          h = -5 * (this.delta - this.prevScore);
          ctx.clearRect(x, this.startY, w, ph);
        } else {
          y = this.startY + -5 * this.prevScore;
          h = -5 * this.delta;
        }
        this.drawRect(ctx, x, y, w, h, "red");

        this.lastx = x;
        this.lasty = y.valueOf();
        this.lastw = 120;
        this.lasth = h.valueOf();
        this.color2draw = "red";
      }
    }

    //show newest part of score
    this.drawRect(
      ctx,
      this.lastx,
      this.lasty,
      this.lastw,
      this.lasth,
      this.color2draw
    );
  }

  setupLabels(ctx, x, w) {
    if (this.game.dispTraj === false) {
      this.drawRect(ctx, x - 10, this.startY, 160, 3, "black");
    }
    ctx.font = "30px CustomFont";

    if (this.printDecomposed === true) {
      if (this.game.dispTraj === false) {
        ctx.font = "40px CustomFont";
        ctx.fillText("Score: $" + String(this.score), 10, 50);

        this.barImg(ctx, "img_gas", -25);
        this.barText(ctx, this.gasScore - this.prevGasScore, 0);

        this.barImg(ctx, "img_total", 10);
        this.barText(ctx, this.pScore - this.prevPScore, 30);
      } else {
        ctx.font = "40px CustomFont";
        ctx.fillStyle = "black";
        ctx.fillText("Score", 10, 50);
        ctx.fillText("Change: $" + String(this.score), 10, 90);

        this.barImg(ctx, "img_gas", -170, 130, 50);
        this.barText(ctx, this.gasScore, -140, "", "30px");

        this.barImg(ctx, "img_total", -100, 130, 50);
        this.barText(ctx, this.pScore, -70, "", "30px");
      }
    } else if (this.decomposedScore === true) {
      ctx.fillStyle = "brown";
      ctx.fillText("Total: $" + String(this.score), 10, 50);
      this.barText(ctx, this.delta, 0);
    } else {
      ctx.fillStyle = "brown";
      ctx.fillText("Score: $" + String(this.score), 10, 50);
      this.barText(ctx, this.delta, 0);
    }
  }

  draw(ctx) {
    this.drawGasTank(ctx, 200);
    let x = 10;
    let w = 140;
    // ctx.fillText("Score: $" + String(this.delta), 10, 100);
    //draw prevscore
    if (this.game.dispTraj === false) {
      this.drawRects(ctx, x, w);
      ctx.clearRect(10, 60, w, -100);
      // ctx.clearRect(10, 600, w, -20);
      ctx.fill();

      this.setupLabels(ctx, x, w);
    } else {
      this.setupLabels(ctx, x, w);
    }
  }

  update() {
    if (
      this.game.vehicle.reachedGoal &&
      this.game.vehicle.goal !== this.goalDrawn
    ) {
      if (this.decomposedScore === true) {
        this.prevScore = this.pScore;
        this.score = this.game.pScore;
      } else {
        this.prevScore = this.score;
        this.score = this.game.score;
      }

      this.prevGasScore = this.gasScore;
      this.gasScore = this.game.gasScore;

      this.prevPScore = this.pScore;
      this.pScore = this.game.pScore;

      this.goalDrawn = this.game.vehicle.goal;
      this.delta = this.score - this.prevScore;
      this.lasth = 0;
    }
  }
}
