const express = require('express');
const http = require('http')
const {PythonShell} = require('python-shell');
const { stringify } = require('querystring');

let pyshell = new PythonShell('server.py', { pythonOptions: ['-u'] });

const app = express();


app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.listen(5000);


pyshell.on('message', function (message) {
    console.log(message);
});


app.get('/start', (req, res) => {
    // let data = {
    //     type: 'initialize',
    //     content: 'teste'
    // }
    var a = ["initialize", "teste"];
    pyshell.send(JSON.stringify(a));
    // JSON.stringify({x: "iniciou"})
    res.send("Ok");
});

app.get('/load', (req, res) => {
    pyshell.send(["chat", "TEste"]);
    res.send("end");
});

