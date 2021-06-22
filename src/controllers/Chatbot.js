const venom = require('venom-bot');
const pyshell = require('python-shell');
const fs = require('fs');
const fetch = require("node-fetch");

module.exports = class Chatbot {
    apresentacao = 'Olá eu sou o *Genuíno* 👴, um robô criado para te auxiliar na checagem de fatos.\n\n' +
    '📰 Basta você me enviar uma notícia e eu direi se ela é falsa ou não.\n' +
    '🟢 Consigo ler mensagens através de capturas de tela (do título da notícia) e também por texto.\n\n' +
    'Quer saber como enviar uma notícia para avaliação? Envie *ajuda* que eu te mostro!';
    
    message;
    client;
    route = "controllers/routes.py";
    python;
    request = { type: "", data: "" };
    

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
        // adicionar listener para quando o robo for adicionado no grupo ele deve se apresentar
        // adicionar listener para quando alguem marca-lo em uma mensagem ele deve passar pelas mesmas etapas do onmessage
        this.client.onMessage((message) => {
            //Verifica se a mensagem é um tipo valido, caso não retorna mensagem do chatbot
            this.setMessage(message);
            this.verifyMessage(this.getClient, message);
        });
    }

    verifyMessage(client, message) {
        let type = message.type;
        let body = message.body;
        if(type == 'chat'){
            if(this.isValidUrl(body)){
                this.get('predict_url', 'url', body);
            }else{
                
                this.get('chat', 'url', body);
            }
        }else if (type == 'image'){
            let base64 = JSON.stringify(val);
            this.get('predict_image', 'url', base64);
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

    createImageJson(val){
        let base64 = JSON.stringify(val);
        fs.writeFile('tokens/base64.json', base64, 'utf8', function(errfs){
            if(errfs){ 
                throw errfs; 
            }else{
                return true;
            }
        });
    }

    async get(route, type = null, data = null){
        let params = (type !== null ? route + "?type=" + type + "&data=" + data : route);

        let fetched = await fetch('http://localhost:3000/' + params)
        .then(res => res.json())
        .catch(err => console.log(err));

        return this.sendToClient(fetched.response);
    }

    async post(route, type, data = null){
          // this.request = {
                //     type: 'url',
                //     data: body
                // };
        var post = JSON.stringify(this.post);

        let fetched = await fetch('http://localhost:3000/' + route, {
            method: 'post',
            body: post,
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(json => console.log(json))
        .catch(err => console.log(err));

        console.log(fetched.response);
    }

    async sendToServer(route){
        // pyshell.PythonShell.run(this.route, this.options, function(err, res){ if(err) throw err; else console.log(res); });
    }

    formatMessage(message){
        let ret = "";
        switch(message){
            case 'fake':
                ret = "❌ A notícia foi considerada FALSA.";
                break;
            case 'true':
                ret = "✅ A notícia foi classificada como VERDADEIRA";
                break;
            case 'retorno':
                ret = "A minha resposta foi útil? Se for possível, dê seu feedback. 😁";
                break;
            default:
                ret = message;
                break;
        }
        return ret;
    }
    
    sendToClient(message){
        message = this.formatMessage(message);
        this.getClient().sendText(this.getReceiver(this.getMessage()), message).catch((err) => { 
            console.error('Error when sending: ', err); 
        });
    }

}