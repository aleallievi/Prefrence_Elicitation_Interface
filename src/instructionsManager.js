import Game from "/src/game";

export default class InstructionManager {
  constructor() {
    this.finishedIns = false;
    this.insScene = 1;
    this.finishedGamePlay = false;
    this.animationGame = new Game(
      600,
      600,
      { x: 0, y: 3 },
      "anim_examp",
      false
    );
    this.animationGame.start(false, true);
    // this.w = 1.252*window.gsWidth;
    // this.h = 0.751*window.gsHeight;
    // this.x = -0.125*window.gsWidth;
    // this.y = 0.083*window.gsHeight;
    // this.w = 750;
    // this.h = 450;
    // this.x = -75;
    // this.y = 50;
  }

  // createButton(canvas, ctx) {}

  update() {

    if (this.insScene === 7 && !this.finishedGamePlay) {
      this.finishedIns = true;

    }
    if (this.insScene === 8 && this.finishedGamePlay && !window.finishedTrajBoard) {
      this.finishedIns = true;
      window.playTrajBoard = true;

    }
    if (this.insScene === 11) {
      this.finishedIns = true;
      window.begunQueries = true;
    }

    this.img = document.getElementById("ins" + String(this.insScene));
    // console.log("here");
  }
  playAnimation(ctx) {
    this.animationGame.update();
    this.animationGame.draw(ctx);
  }
  draw(ctx) {
    if (this.insScene === 7 && !this.finishedGamePlay) return;
    if (this.insScene === 11) return;
    if (this.insScene === 4) {
      this.playAnimation(ctx);
      // this.h = 0.333*window.gsWidth;
      // this.w = 1.166*window.gsWidth;
      // this.x = -0.0666*window.gsWidth;
      // this.y = -0.0166*window.gsWidth;
      this.h = 200;
      this.w = 700;
      this.x = -40;
      this.y = -10;
    } else {
      //TODO: WE ONLY WANT TO DO THIS ON LOAD
      // if (!window.resizing) {
      //   this.w = 1.252*window.gsWidth;
      //   this.h = 0.751*window.gsWidth;
      //   this.x = -0.125*window.gsWidth;
      //   this.y = 0.083*window.gsWidth;
      //
      //
      // }

      //
      this.w = 750;
      this.h = 450;
      this.x = -75;
      this.y = 50;
    }

    ctx.drawImage(this.img, this.x, this.y, this.w, this.h);
    //draw button
    // ctx.fillStyle = "white";
    // ctx.beginPath();
    // ctx.rect(500, 550, 100, 50);

    // ctx.font = String(0.04166*window.gsWidth) + "px CustomFont";
    ctx.font = "20px CustomFont";

    ctx.fillStyle = "gray";

    // console.log("here");
    if (this.insScene === 6) ctx.fillText("Play", 500, 570);
    else if (this.insScene === 7) ctx.fillText("Play", 500, 570);
    else if (this.insScene === 10) ctx.fillText("Begin", 500, 570);
    else ctx.fillText("Next",500, 570);
    //500, 570
    //
    ctx.fill();
  }
}
