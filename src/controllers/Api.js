const express = require('express');
const http = require('http')


const app = express();


app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.listen(5000);