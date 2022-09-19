// Importing the required modules
const WebSocketServer = require('ws');
 
// Creating a new websocket server
const wss = new WebSocketServer.Server({ port: 3154 })
 
var movecount = 0;
var grid = new Array(19);
var arr = new Array(19*19);

function checkwin() {
    for(var i = 0; i < 19*19; i++) {
        if(arr[i] == null) continue;
        
        var now = arr[i] ;
        //horizontal 
        if(i % 19 <= 15) {
            var flag = true;
            for(var j = i; j <= i+4; j++) {
                if(arr[j] != now) {
                    flag = false
                    break;
                }
            }
            if(flag == true) return now;
        }
        //vertical
        if(i / 19 <= 15) {
            var flag = true;
            for(var j = i; j <= i+4*19; j += 19) { 
                if(arr[j] != now) {
                    flag = false
                    break;
                }
            }
            if(flag == true) return now;
        }

        //left diagonal
        if(i % 19 >= 4 && i / 19 <= 15) {
            var flag = true;
            for(var j = i; j <= i + 4*18; j += 18) {
                if(arr[j] != now) {
                    flag = false
                    break;
                }
            }
            if(flag == true) return now;
        }
        if(i % 19 <= 15  && i / 19 <= 15) {
        //right diagonal
            var flag = true;
            for(var j = i; j <= i + 4*20; j += 20) {
                if(arr[j] != now) {
                    flag = false
                    break;
                }
            }
            if(flag == true) return now;
        }
    }
    return null;
}

for (let i = 0; i < grid.length; i++) {
    grid[i] = new Array(19);
}

var number_of_players = 0;
wss.on("connection", ws => {
     
     console.log("new client connected");
     gridstate = {type: "grid"}
     ws.on("message", e => {
        
        console.log(`Client has sent us: ${e}`)
        var data = JSON.parse(e); 
        var x = data.x;
        var y = data.y;
        //console.log('x = '+x);
        //console.log('y = '+y);
        
        if (grid[x / 30][y / 30] != null) {
            const obj = {type: "move", res: false}
            wss.broadcast(JSON.stringify(obj))
        }
        else {
            if (movecount % 2 == 0) {
              grid[x / 30][y / 30] = 1;
              arr[x/30 + y/30*19] = 1;
              console.log('placed stone at ' + x + ' y = '+y);
            } else {
              grid[x / 30][y / 30] = 0;
              arr[x/30 + y/30] = 0;
            }
            movecount++;
            var color = 'white';
            if(movecount % 2 == 1) {
                color = 'black';             
            }
            const obj = { type: "move", x: x, y: y, color: color, res: true};
            wss.broadcast(JSON.stringify(obj));
            console.log("move successful, color is"+color)
            
            if(checkwin() != null) {
                winner = checkwin()
                const obj = { type: "winner", who: winner};
                wss.broadcast(JSON.stringify(obj));
                console.log("winner is" + winner);
            }
        }
    });
    
    ws.on("close", () => {
        console.log("client disconnected");
    });
});

wss.broadcast = function broadcast(msg) {
   console.log(msg);
   wss.clients.forEach(function each(client) {
       client.send(msg);
    });
};
    
console.log("The WebSocket server is running on port 3154");
