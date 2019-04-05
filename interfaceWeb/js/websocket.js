var socketPrism;
var password = false;
var light;

const url = "ws://localhost:8080";

var loginScreen = document.getElementById("login");
var errorScreen = document.getElementById("error");
var contentScreen = document.getElementById("content");

socketPrism = new WebSocket(url);

socketPrism.onopen = function(event) 
{ }
socketPrism.onmessage = function (event) {
    console.log(event)
    if (event.data == "OK") {
        loginScreen.style = "display: none;";
        errorScreen.style = "display: none;";
        contentScreen.style = "";
    } else if (event.data == "ER") {
        loginScreen.style = "display: none;";
        contentScreen.style = "display: none;";
        errorScreen.style = "";
    }
}
