const title_container = document.querySelector(".title_container");
const letter = document.querySelectorAll("img");
const app = document.querySelectorAll(".app");
const link = document.querySelector(".link");
var move;

function gathering() {
    console.log(letter.length);

    app.forEach(app => {
        

        var app_top = app.getBoundingClientRect().top;
        var app_left = app.getBoundingClientRect().left;

        app_top += 30;
        app_left += 30;

        console.log("app_top" + app_top);
        console.log("app_left" + app_left);
        
        move = {
            top: `${app_top}px`,
            left: `${app_left}px`,
            transform: `scale(0)`,
        };
        
    });

    letter.forEach(lt => {

        var top = lt.getBoundingClientRect().top
        var left = lt.getBoundingClientRect().left

        console.log("top" + top);
        console.log("left" + left);

        lt.classList.remove("img_1");
        lt.classList.remove("img_2");
        lt.classList.remove("img_3");
        lt.classList.remove("img_4");
        lt.classList.remove("img_5");
        lt.classList.remove("img_6");
        lt.classList.remove("img_7");
        lt.classList.remove("img_8");
        lt.classList.remove("img_9");
        lt.classList.remove("img_10");

        console.log("top" + top);
        console.log("left" + left);

        lt.style.top = top + "px"
        lt.style.left = left + "px"

        lt.classList.add("shaking");

    });

    setTimeout(function() {

        letter.forEach(lt => {
            lt.animate(move, {
                duration: 1000,
                fill: "forwards",
            });
        });

        title_container.classList.add("invisible");

    }, 500);
    
    setTimeout(function() {

        console.log(link);
        link.click();

    }, 1500);
    

}