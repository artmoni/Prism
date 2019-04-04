var socketPrism;
var password = new Boolean("false");
var light;

const url = "ws://localhost";

socketPrism = new WebSocket(url);

socketPrism.onopen = function(event) 
{
    socketPrism.send("Authentification"); 

    password = event.data;

    if(!password)
    {
        print("Access authorized");
        light = "G";
        send(light);
    }
    else if(password)
    {
        print("Access denied");
        light = "R";
        send(light);
    }
}

function logOut()
{
    socketPrism.close();
}