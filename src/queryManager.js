import QueryInputHandler from "/src/queryInput";

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

    this.offset = 500;
    this.b1_x = 200+(420/2)-(70/2)-100
    this.b1_y = 600
    this.b1_h = 50
    this.b1_w = 70
    this.b2_x = 290+this.offset+(420/2)-(70/2)-100
    this.b3_x = 720-160/2-100
    this.b3_y = 600
    this.b3_h = 130
    this.b3_w = 50
    this.b4_y = 500
    new QueryInputHandler();
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
    // window.canvas.width = window.innerWidth;
    // window.canvas.height = window.innerHeight;
    // window.canvas.width = 1200;
    // window.canvas.height = 700;
    window.canvas.style.display = "none"
    this.started = true;
    this.queryResults = {}
    this.lastDeltaTime = deltaTime;
    $("#myModal").on('show.bs.modal', function (e) {
       var modal = $(this)
       // modal.find('.label1').text(ins)
       // modal.find('.modal_img1').attr("src","assets/images/img_flag.png")
       $(".img-responsive").attr('src', "https://raw.githubusercontent.com/Stephanehk/Prefrence_Elicitation_Interface/main/assets/images/query_ins.png");
       //modal_img1

    });
    $("#myModal").modal("show");
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


    this.drawButton(ctx,this.b1_x,this.b1_y,this.b1_w,this.b1_h,this.b1Color,"Left",this.b1_x-(this.b1_w/2)+45,this.b1_y+(this.b1_h/2)+5)
    this.drawButton(ctx,this.b2_x,this.b1_y,this.b1_w,this.b1_h,this.b2Color,"Right",this.b2_x-(this.b1_w/2)+45,this.b1_y+(this.b1_h /2)+5)


    this.drawButton(ctx,this.b3_x,  this.b3_y,this.b3_h,this.b3_w,this.b3Color,"Same",this.b3_x+(this.b3_h/2)-25,  this.b3_y+(this.b3_w/2)+5)
    this.drawButton(ctx,this.b3_x,this.b4_y,this.b3_h,this.b3_w,this.b4Color,"Can't Tell",  this.b3_x+(this.b3_h/2)-50,this.b4_y+(this.b3_w/2)+5)

    // this.drawButton(ctx,315-8+offset-65,590-200,130,50,this.b4Color,"Can't Tell",315-8+15+offset-65,510+30+80-200)

    ctx.drawImage(
      this.img1,
      200-100,
      10,
      420,
      550
    );

    ctx.drawImage(
      this.img2,
      290+this.offset-100,
      10,
      420,
      550
    );

  }
}
