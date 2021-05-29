let imgs1 = document.getElementById("imgs1");
let imgs2 = document.getElementById("imgs2");
let imgs3 = document.getElementById("imgs3");
let txt = document.getElementById("current-text");

function toggleMenu1() {
    document.getElementById("dropdown-content-id").classList.toggle("hideContent");
}

function toggleImgs1() {
    if (imgs1.classList.contains("hideContent") === true) {
        imgs1.classList.remove("hideContent");
    }
    if (imgs2.classList.contains("hideContent") == false) {
        imgs2.classList.add("hideContent");
    }
    if(imgs3.classList.contains("hideContent") == false) {
        imgs3.classList.add("hideContent");
    }
    txt.innerHTML = "Landscape pictures."
}

function toggleImgs2() {
    if (imgs2.classList.contains("hideContent") === true) {
        imgs2.classList.remove("hideContent");
    }
    if (imgs1.classList.contains("hideContent") == false) {
        imgs1.classList.add("hideContent");
    }
    if(imgs3.classList.contains("hideContent") == false) {
        imgs3.classList.add("hideContent");
    }
    txt.innerHTML = "Event pictures."
}

function toggleImgs3() {
    if (imgs3.classList.contains("hideContent") === true) {
        imgs3.classList.remove("hideContent");
    }
    if (imgs2.classList.contains("hideContent") == false) {
        imgs2.classList.add("hideContent");
    }
    if(imgs1.classList.contains("hideContent") == false) {
        imgs1.classList.add("hideContent");
    }
    txt.innerHTML = "Art pictures."
}