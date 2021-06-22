const express = require('express');
const http = require('http')
const async = require('async');
const {PythonShell} = require('python-shell');
const { stringify } = require('querystring');
const fs = require('fs');
const chat = JSON.parse(fs.readFileSync('../lib/chatting/chat.json', 'utf8'));
let pyshell = new PythonShell('server.py', { pythonOptions: ['-u'] });
const app = express();
const globalRes = {};

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

pyshell.on('message', function (message) {
    if(message !== 'started')
        globalRes.res.status(200).json({ response: message });
    else
        console.log(message);
});

let createRequest = (type, data) => {
    return JSON.stringify({"type": type, "data": data});
}

app.listen(3000, () => {
    try{
        let data = createRequest("start", null);
        pyshell.send(data);
    }catch(error){
        console.log("Erro ao iniciar o servidor python: " + error);
    }
});


app.get('/chat', async(req, res) => {
    console.log(req.query.type);
    console.log(req.query.data);

    try{
        let string = req.query.data;
        string = string.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
        res.status(200).json({ response: chat[string] });
    }catch(error){
        res.status(500).json({ response: 'error' });
    }
});


app.get('/predict_image', async(req, res) => {
    let data = createRequest(req.query.type, req.query.data);
});

app.get('/predict_url', async(req, res) => {
    console.log(req.query.type);
    console.log(req.query.data);
    let data = createRequest(req.query.type, req.query.data);

    try{
        pyshell.send(data);
        globalRes.res = res;
    }catch(error){
        res.status(500).json({ response: 'error' });
    }
});