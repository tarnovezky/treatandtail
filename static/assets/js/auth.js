let signbtt = 0;
let regbtt = 0;
let bar = 0;

let login = 0;
let registr = 0;

let remember = 0;
let checked = 0;

let currentbtt = 0;

let authBlock = document.getElementById("auth");

signbtt = document.getElementById("signin");
regbtt = document.getElementById("reg");
bar = document.getElementById("underLn");

login = document.getElementById("login");
registr = document.getElementById("registr");

remember = document.getElementById("remembercheckbox");

let invert = -1;

login.style.marginLeft = "0%";
registr.style.marginLeft = -100 * invert + "%";
bar.style.width = "31%";
bar.style.marginLeft = "0%";

regbtt.addEventListener("click", () => {if(currentbtt == 0) {currentbtt = 2; tweenService.tween(bar, tweenService.createParam([["marginLeft", 39, "%"],["width", 54, "%"]]), 100, "linear");
    tweenService.tween(registr, tweenService.createParam([["marginLeft", 0, "%"]]), 100, "linear");
    tweenService.tween(login, tweenService.createParam([["marginLeft", invert * 100, "%"]]), 100, "linear"); currentbtt = 1;}})
signbtt.addEventListener("click", () => {if(currentbtt == 1) {currentbtt = 2; tweenService.tween(bar, tweenService.createParam([["marginLeft", 0, "%"],["width", 31, "%"]]), 100, "linear");
    tweenService.tween(registr, tweenService.createParam([["marginLeft", invert * -100, "%"]]), 100, "linear");
    tweenService.tween(login, tweenService.createParam([["marginLeft", 0, "%"]]), 100, "linear"); currentbtt = 0;}})

remember.addEventListener("click", () => {
    if (checked == 0) {checked = 1; remember.innerHTML = "✔";} else {checked = 0; remember.innerHTML = " "}
})



const tweenService = {

    //Creates object with parameters for tween function.
    //Takes an 2D array with paramaters of an object that is meant to be animated,
    //its destination value (0 if no value is passed) and units (" " if no value is passed)
    //Format of the array that shloud be passed [["parameter",destination value,"units"],["parameter",destination value,"units"], ... , ["parameter",destination value,"units"]]

    createParam: function(pArr) {
        let tweenPObj = {};
        for(let i = 0; i < pArr.length; i++) {
            if(pArr[i][0]){
                let elemArr = [];
                elemArr[0] = pArr[i][1] || "0";
                elemArr[1] = pArr[i][2] || " ";
                tweenPObj[pArr[i][0]] = elemArr;
            }
        }
        return tweenPObj;
    },

    easing: function(i, a, t, time) {
        type = t || "linear";
        time--;
        if(type == "linear"){
            return (a/time)*i;
        } else if (type == "sinein") {
            return a * Math.sin(i/time * (Math.PI / 2));
        } else if (type== "sineout") {
            return a * (-Math.sin((1-i/time) * (Math.PI / 2)) + 1);
        } else if (type=="sineinout"){
            // if(i < time/2) {
            //     return a * (-Math.sin((1-i/time) * (Math.PI /2)) + 1) * 1.78;
            // } else {return a * Math.pow((Math.sin((i/time) * (Math.PI /2))), 2) ;}
            let tm = i / time;
            return a * (Math.sin(Math.PI * tm - Math.PI / 2) + 1) / 2;
        }
    },

    //Tweening function takes object to be animated, parameters object, time (speed). Parameters object created using tweenService.createParam(...)

    tween: function(obj, prm, speed, easing) {
        let time = 1000/speed,
        // easing = easing || "linear",
        initialV = {};
        for(let key in prm) {
            initialV[key] = obj.style[key];
            console.log(initialV[key]);
            let delta = (parseFloat(prm[key][0]) - parseFloat(obj.style[key]));
            prm[key].push(delta);
        }
        let i = 0;
        function animate() {
            for(let key in prm){
                obj.style[key] = parseFloat(initialV[key]) + tweenService.easing(i,parseFloat(prm[key][2]),easing, time) + prm[key][1];
            }
            i++;
            if (i <= time-1) {
                setTimeout(animate, 1000 / 60); // 60 fps
            }
        }
        animate();
        console.log(prm);
    },

    //Set object values that is going to be tweened using this function in the very beginning. It is neccesary to do so for tweenSevice to work properly.
    //Takes obj which is object that is going to be tweened in future, and parameters of this object with their initial values that is going to be tweened during runtime.

    setParams: function(obj, pArr) {
        if(obj[1]) {
            for(let o = 0; o<obj.length; o++) {
                for(let i = 0; i<pArr.length; i++) {
                    obj[o].style[String(pArr[i][0])] = String(pArr[i][1]);
                }
            }
            return;
        }
        for(let i = 0; i<pArr.length; i++) {
            obj.style[String(pArr[i][0])] = String(pArr[i][1]);
        }
    }
}








