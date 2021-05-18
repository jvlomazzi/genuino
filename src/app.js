const venom = require('venom-bot');
const pyshell = require('python-shell');
const Chatbot = require('./controllers/Chatbot');

// function start(client) {
// 	client.onAnyMessage((message) => {
// 		let options = {
// 			pythonOptions: ['-u'],
// 			args : ['news', message.body]
// 		}
// 		pyshell.PythonShell.run('routes.py', options, function(err, res){
// 			if(err)	throw err;

// 			console.log(res)
// 		});
// 		if (message.body === '--bot apresentação') {
// 			// let from = message.isGroupMsg ? message.chatId : message.from;
// 			let from = message.chatId;
// 			client
// 				.sendImage(from,
// 					'assets/genuino-profile-picture.jpg',
// 					'Genuíno',
// 					'teste')
// 				.then((result) => {
// 					console.log('Result: ', result); //return object success
// 				})
// 				.catch((erro) => {
// 					console.error('Error when sending: ', erro); //return object error
// 				});
// 		}
// 	});
// }

// let options = {
// 	pythonOptions: ['-u'],
// 	args : ['news', message.body]
// }
venom.create().then((client) => {
	const chatbot = new Chatbot(client);
	// pyshell.PythonShell.run('routes.py', options, function(err, res){
	// 	if(err)	throw err;
	// 	console.log(res)
	// });
}).catch((erro) => {
	console.log(erro);
});