const venom = require('venom-bot');
const pyshell = require('python-shell');
const fs = require('fs');

module.exports = class Chatbot {
    apresentacao = 'Olá eu sou o *Genuíno* 👴, um robô criado para te auxiliar na checagem de fatos.\n\n' +
    '📰 Basta você me enviar uma notícia e eu direi se ela é falsa ou não.\n' +
    '🟢 Consigo ler mensagens através de capturas de tela (do título da notícia) e também por texto.\n\n' +
    'Quer saber como enviar uma notícia para avaliação? Envie *ajuda* que eu te mostro!';
    
    message;
    client;
    route = "controllers/routes.py";
    python;
    options = {
        pythonOptions: ['-u'],
        args : []
    }
    

    constructor(){
        venom.create().then((client) => {
            this.setClient(client);
            this.listen();
        }).catch((err) => console.log(err));
    }

    setClient(client){
        this.client = client;
    }

    getClient(){
        return this.client;
    }

    getApresentacao() {
        return this.apresentacao;
    }


    
    /**
     * Verifica se é uma mensagem de resposta imediata, como por exemplo "Olá", "Ajude-me".
     * Mensagens de respostas NÃO imediatas podem ser enviadas seguidas de um link, fazendo com que o chatbot pule uma etapa.
     */
    // isImmediateAnswer(){
        
    // }
    setEmptyArgs(){  
        this.options.args = [];
    }
    /**
     * 
     * @param {*} args Pode ser utilizado quantas vezes for necessário, porém,
     * a primeira chamada para definir o argumento deve ser para definir o nome da rota.
     */
    setServerArgs(args){
        this.options.args.push(args);
    }
    
    setMessage(message) {
        this.message = message;
    }
    
    getMessage() {
        return this.message;
    }
    
    getReceiver(message){
        let res;
        if(message.isGroupMsg){
            res = message.chatId;
        }else{
            res = message.from;
        }
        return  res;
    }

    listen()
    {
        this.startBackendServer();
        // adicionar listener para quando o robo for adicionado no grupo ele deve se apresentar
        // adicionar listener para quando alguem marca-lo em uma mensagem ele deve passar pelas mesmas etapas do onmessage
        this.client.onMessage((message) => {
            //Verifica se a mensagem é um tipo valido, caso não retorna mensagem do chatbot
            this.verifyMessage(this.getClient, message);
        });
    }

    startBackendServer(){
        this.setServerArgs('initialize');
        this.sendToServer();
    }
    
    verifyMessage(client, message) {
        let type = message.type;
        let body = message.body;
        if(type == 'chat'){
            if (this.isValidUrl(body)){
                console.log("chegou url");
                this.setEmptyArgs();
                this.setServerArgs('url');
                this.setServerArgs(body);
            }else{
                console.log("chegou chat");
                this.setEmptyArgs();
                this.setServerArgs('chat');
                this.setServerArgs(body);
            }
            
            this.sendToServer();
        }else if (type == 'image'){
            this.sendImageToServer(message);
        }else{
            throw "Invalid message type";
        }
    }

    isValidUrl(str) {
        var pattern = new RegExp('^(https?:\\/\\/)?'+
            '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+
            '((\\d{1,3}\\.){3}\\d{1,3}))'+
            '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+
            '(\\?[;&a-z\\d%_.~+=-]*)?'+
            '(\\#[-a-z\\d_]*)?$','i');
        return !!pattern.test(str);
    }

    async sendImageToServer(message){
        var promise = this.client.downloadMedia(message.id);
        var chat = this;
        await promise.then(function(val){
            chat.setMessage(val);
            let base64 = JSON.stringify(val);
            fs.writeFile('tokens/base64.json', base64, 'utf8', function(errfs){
                if(errfs){ 
                    throw errfs; 
                }else{
                    chat.setServerArgs('image');
                    chat.sendToServer();
                }
            });
        }).catch(function(err){
            console.log(err)
        });
    }

    async sendToServer(){
        pyshell.PythonShell.run(this.route, this.options, function(err, res){ if(err) throw err; else console.log(res); });
    }
    
    sendToClient(){
        this.getClient().sendText(this.getReceiver(this.getMessage), this.getMessage).then((result) => {
             console.log('Result: ', result); 
        }).catch((err) => { 
            console.error('Error when sending: ', err); 
        });
    }

}