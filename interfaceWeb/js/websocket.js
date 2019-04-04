var socketPrism;
var password = new Boolean("false");
var light = new Boolean("false");

const url = "ws://localhost";

function connect() 
{
    socketPrism = new WebSocket(url);

    socketPrism.onopen = function (event) 
    {
        socketPrism.send("Authentification"); 
    };
}

function readData()
{
    socketPrism = new WebSocket(url);

    if(!password)
    {
        print("Access authorized");
        light = "true";

        socketPrism.onopen = function (event) 
        {
            socketPrism.send(light); 
        };
    }
}

function logOut()
{
    socketPrism.close();
}