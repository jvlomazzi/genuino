const express = require('express');
const http = require('http')
const async = require('async');
const {PythonShell} = require('python-shell');
const { stringify } = require('querystring');

let pyshell = new PythonShell('server.py', { pythonOptions: ['-u'] });

const app = express();
globalRes = {};

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.listen(3000);



app.post('/', async(req, res) => {
    let data = JSON.stringify({"type": req.body.type, "data": req.body.data});
    // pyshell.on('message', function (message) { res.status(200).json({ response: 'ok' }); });
    // pyshell.on('message', function (message) { console.log(message) });
    pyshell.send(data);
    globalRes.res = res;
    // await new Promise(() => {
    //     // pyshell.on('message', function (message) { res.status(200).json({ response: 'ok' }); });
    //     pyshell.send(data)
    // }).then( (result) => {
    //     res.status(200).json({ response: 'ok' });
    // }).catch((error) => {
    //     res.status(500).json({ response: 'error' });
    // });
    // try {
    //     await pyshell.send(data).end(function(err){
    //         if (err) handleError(err);
    //         else res.status(200).json({ response: 'ok' });
    //     })
        
    // } catch (error) {
    //     res.status(500).json({ response: 'error' });
    // }
});


pyshell.on('message', function (message) { 
    console.log(message); 
    globalRes.res.status(200).json({ response: 'ok' }); 
});