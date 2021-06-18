
export default class InstructionManager {

  constructor() {
    this.n_query = 0;
    // this.img = document.getElementById("img_ow_tile");
    this.nTrajs = 3;
    this.traj = 1;
    this.started = false;
    this.pressed = false;
    // ASSIGNS THE URL PARAMETERS TO JAVASCRIPT VARIABLES
    this.assignmentID = this.turkGetParam('assignmentId');
    this.b1Color = "grey";
    this.b2Color = "grey";
    this.b3Color = "grey";
    this.b4Color = "grey";
    this.isSubmitted = false;
  }

  turkGetParam( name ) {
    let fullurl = window.location.href;
    var regexS = "[\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var tmpURL = fullurl;
    var results = regex.exec( tmpURL );
    if( results == null ) {
        return "";
    } else {
        return results[1];
    }
}

  start(deltaTime) {
    window.canvas.width = window.innerWidth;
    window.canvas.height = window.innerHeight;
    this.started = true;
    this.queryResults = {}
    this.lastDeltaTime = deltaTime;
  }

  submit() {
    // console.log(this.assignmentID);
    if (!this.isSubmitted) {
      document.getElementById('assignmentId').value = this.assignmentID

      // for (var key in this.queryResults) {
      //   document.getElementById('foo').value = this.queryResults[key]
      //
      // }
      // document.forms[0].submit()
      document.getElementById('hitForm').submit();
      this.isSubmitted = true;
    }


  }

  resetButtons() {
    this.b1Color = "grey";
    this.b2Color = "grey";
    this.b3Color = "grey";
    this.b4Color = "grey";

  }

  queried(data) {
    // this.queryResults["traj" + String(this.traj)] = data;
    if (data === "left")this.b1Color = "black";
    if (data === "right")this.b2Color = "black";
    if (data === "same")this.b3Color = "black";
    if (data === "dis")this.b4Color = "black";

    document.getElementById('query'+ String(this.traj)).value = data

  }

  update(deltaTime) {
    if (!this.started)this.start(deltaTime);
    // console.log(deltaTime -  this.lastDeltaTime);
    if (deltaTime -  this.lastDeltaTime > 200){
      this.resetButtons();
      this.lastDeltaTime = deltaTime;
    }
    if (this.pressed){
      // console.log("pressed");
      // console.log(this.traj);
      if (this.traj === this.nTrajs) {
        this.submit();
      } else {
        this.traj+=1;
        this.pressed = false;
      }
    }
    // this.img.src = "/assets/trajImages/(0,2)_0_1.png"
    let trajId1 = "traj" + String(this.traj) + "0";
    let trajId2 = "traj" + String(this.traj) + "1";
    this.img1 = document.getElementById(trajId1);
    this.img2 = document.getElementById(trajId2);

  }

  drawButton(ctx, x, y, w, h, color,text,tx,ty) {
    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
    ctx.stroke();
    ctx.font = "20px CustomFont";
    ctx.fillStyle = "white";
    ctx.fillText(text, tx,ty);
    ctx.fill();

  }

  // postRequest(data) {
  //
  //   router.post('https://workersandbox.mturk.com/mturk/externalSubmit',function(req,res,next) {
  //     var id = req.params.id;
  //     res.redirect("/test/...");
  //   });
  // }

  draw(ctx) {
    let offset = 450;
    this.drawButton(ctx,215+8+offset-65,530-200,70,50,this.b1Color,"Left",215+8+12+offset-65,450+30+80-200)
    this.drawButton(ctx,315-8+offset-65,530-200,70,50,this.b2Color,"Right",315-8+10+offset-65,450+30+80-200)

    this.drawButton(ctx,155+8+offset-65,590-200,130,50,this.b3Color,"Same",155+8+38+offset-65,510+30+80-200)
    this.drawButton(ctx,315-8+offset-65,590-200,130,50,this.b4Color,"Can't Tell",315-8+15+offset-65,510+30+80-200)

    // ctx.drawImage(
    //   this.img1,
    //   150,
    //   -10,
    //   650,
    //   500
    // );
    //
    // ctx.drawImage(
    //   this.img2,
    //   340+offset,
    //   -10,
    //   650,
    //   500
    // );

  }
}
