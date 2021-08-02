import Game from "/src/game";

export default class InstructionManager {
  constructor() {
    this.finishedIns = false;
    this.insScene = 1;
    this.finishedGamePlay = false;
    this.animationGame1 = new Game(
      600,
      600,
      { x: 0, y: 3 },
      "ins_4_board",
      false
    );
    this.animationGame1.start("",false,true,true,1);

    this.animationGame2 = new Game(
      600,
      600,
      { x: 4, y: 5 },
      "ins_8_board",
      false
    );
    this.animationGame2.start("",false,true,true,2);

  }

  // createButton(canvas, ctx) {}

  update() {

    if (this.insScene === 10 && !this.finishedGamePlay) {
      this.finishedIns = true;
    }
    if (this.insScene === 11 && this.finishedGamePlay && !window.finishedTrajBoard) {
      this.finishedIns = true;
      window.playTrajBoard = true;

    }
    if (this.insScene === 14) {
      this.finishedIns = true;
      window.begunQueries = true;
    }

    //skips instruction where user explores gated area
    if (this.insScene == 8) this.insScene +=1;

    this.img = document.getElementById("ins" + String(this.insScene));

	// this.img.setAttribute('width',  66);
	// this.img.setAttribute('height',  66);

    // $("#ins" + String(this.insScene)).show();
    // console.log("here");
  }
  playAnimation(ctx,id) {
    if (id === 1) {
      this.animationGame1.update();
      this.animationGame1.draw(ctx);
      // if (this.animationGame1.reached_terminal && ctx.globalAlpha > 0.5)ctx.globalAlpha-=0.001
    } else if (id === 2) {
      this.animationGame2.update();
      this.animationGame2.draw(ctx);
      // if (this.animationGame2.reached_terminal && ctx.globalAlpha > 0.5)ctx.globalAlpha-=0.001
      //ctx.globalAlpha = 1;
    }

  }
  draw(ctx) {
    this.pa1 = false;
    this.pa2 = false;
    if (this.insScene === 10 && !this.finishedGamePlay) return;
    if (this.insScene === 14) return;
    if (this.insScene === 4) {
      this.pa2 = true;
    }
    if (this.insScene === 5) {
      this.pa1 = true;

      // this.h = 0.333*window.gsWidth;
      // this.w = 1.166*window.gsWidth;
      // this.x = -0.0666*window.gsWidth;
      // this.y = -0.0166*window.gsWidth;
      // this.h = 200;
      // this.w = 700;
      // this.x = -40;
      // this.y = -10;
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

    // $("#ins" + String(this.insScene)).show();
    if (this.pa1)this.playAnimation(ctx,1);
    if (this.pa2)this.playAnimation(ctx,2);
    //draw button
    // ctx.fillStyle = "white";
    // ctx.beginPath();
    // ctx.rect(500, 550, 100, 50);

    // ctx.font = String(0.04166*window.gsWidth) + "px CustomFont";
    ctx.font = "20px CustomFont";

    ctx.fillStyle = "gray";

    // console.log("here");
    if (this.insScene === 9) ctx.fillText("Play", 500, 570);
    else if (this.insScene === 10) ctx.fillText("Play", 500, 570);
    else if (this.insScene === 13) ctx.fillText("Begin", 500, 570);
    else ctx.fillText("Next",500, 570);
    //500, 570
    //
    ctx.fill();
  }
}
