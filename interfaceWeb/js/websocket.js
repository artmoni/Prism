var socketPrism;
var password = new Boolean("false");
var light;

const url = "ws://localhost";

socketPrism = new WebSocket(url);

socketPrism.onopen = function(event) 
{
    socketPrism.send("Authentification"); 
}

function readData()
{
    if(!password)
    {
        print("Access authorized");
        light = "G";
    }
    else if(password)
    {
        print("Access denied");
        light = "R";
    }
}

function logOut()
{
    socketPrism.close();
}