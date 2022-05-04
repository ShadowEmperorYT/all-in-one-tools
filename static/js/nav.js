let menu = document.querySelector("#menu");
let menu_bar = document.querySelector("#menu-bar");

const activeMenuBar = ()=>{
    menu.classList.toggle('menu-toggle');
}

menu_bar.addEventListener("click", activeMenuBar);