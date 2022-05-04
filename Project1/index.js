const http = require('http');
const msgpack = require('msgpack5')();
const mysql = require('mysql');
const sd = require('silly-datetime');
const json = require('json');

const dbServer = mysql.createConnection({
  host: 'localhost',
  port: '3306',
  user: 'debian-sys-maint',
  password: 'v6MTpMVWsMOOGWNB',
  database: 'network_lab1'
});

const webServer = http.createServer((req, res) => {
  const chunks = [];
  let size = 0;

  req.on('data', (chunk) => {
    chunks.push(chunk);
    size += chunk.length;
  });

  req.on('end', () => {
    let data = null;
    switch (chunks.length) {
      case 0: data = chunks[0];
        break;
      case 1: data = chunks[0];
        break;
      default:
        data = new Buffer(size);
        for (let i = 0, pos = 0, len = chunks.length; i < len; i++) {
          const chunk = chunks[i];
          chunk.copy(data, pos);
          pos += chunk.length;
        }
        break;
    }

    if (data == null) {
        return;
    }

    //console.log(data)
    data = msgpack.decode(data);//dict
    console.log(data.mac);
    try{
      {
        let addSql = 'INSERT INTO msg(Time,GatewayMAC,DeviceUUID,RSSI) VALUES(?,?,?,?)';
        let addSqlParams = new Array();

        const Time = sd.format(new Date(), 'YYYY-MM-DD HH:mm:ss');
        const GatewayMAC = data['mac'];
        const DeviceUUID = 'b0702880a295a8abf734031a98a512de';
        let RSSI = 0;
        let num = 0;
        addSqlParams.push(Time);
        addSqlParams.push(GatewayMAC);
        addSqlParams.push(DeviceUUID);

        let len = data['devices'].length;//arrayLength
        for(let i = 0; i < len; i++){
          const frame = data['devices'][i];//Buffer
          /*const DeviceMAC = frame.slice(1, 7).toString('hex');
          if(DeviceMAC !== '7e460ea52948'){
            continue;
          }
          console.log(frame);*/
          const DeviceUUID = frame.slice(17,33).toString('hex');
          if(DeviceUUID !== 'b0702880a295a8abf734031a98a512de'){
            continue;
          }
          //console.log(parseInt(frame.slice(7, 8).toString('hex'), 16) - 256);
          RSSI += (parseInt(frame.slice(7, 8).toString('hex'), 16) - 256);
          num++;
        
        }
        RSSI /= num;
        addSqlParams.push(RSSI);
        dbServer.query(addSql, addSqlParams, function(err, result) {
          if(err){
            console.log('[INSERT ERROR] - ', err.message);
            return;
          }
        });
      }
      res.end('post')
    }
    catch(e){
      console.log(e.name + " : " + e.message)
      res.end(e.name + " : " + e.message);
    }
  });
});

dbServer.connect();
webServer.listen(80);