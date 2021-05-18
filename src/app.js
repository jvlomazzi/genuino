const venom = require('venom-bot');
const pyshell = require('python-shell');
const Chatbot = require('./controllers/Chatbot');

venom.create().then((client) => {
	const chatbot = new Chatbot(client);
}).catch((erro) => {
	console.log(erro);
});