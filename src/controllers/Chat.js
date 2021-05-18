const pyshell = require('python-shell');
const fs = require('fs');
module.exports = class Chat {
    apresentacao = 'Olá eu sou o *Genuíno* 👴, um robô criado para te auxiliar na checagem de fatos.\n\n' +
    '📰 Basta você me enviar uma notícia e eu direi se ela é falsa ou não.\n' +
    '🟢 Consigo ler mensagens através de capturas de tela (do título da notícia) e também por texto.\n\n' +
    'Quer saber como enviar uma notícia para avaliação? Envie *ajuda* que eu te mostro!';
    
    message;

    options = {
        // scriptPath: 'src/controllers',
        pythonOptions: ['-u'],
        args : []
    }
    

    constructor(client){
        this.init(client);
    }

    init(client)
    {
        client.onMessage((message) => {
            //Verifica se a mensagem é um tipo valido, caso não retorna mensagem do chatbot
            // let image = this.imageMessageControl(client, message);
            // if(!image){
                this.verifyMessage(client, message);
            // }
            // client.sendText(this.getReceiver(message), this.getMessage)
            //     .then((result) => { console.log('Result: ', result); })
            //     .catch((erro) => { console.error('Error when sending: ', erro); });

        });
    }

    getApresentacao() {
        return this.apresentacao;
    }

    
    verifyMessage(message) {
        let type = message.type;
        let body = message.body;
        switch(type){
            case 'text':
                console.log("uepa")
                break;
            case 'image':
                break;
            default:
                console.log("Tipo invalido de mensagem.")
                break;
        }
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

    imageMessageControl(client, message) {
        let type = message.type;

        if(type == 'image'){
            this.getImageFromMessage(client, message);
            return true;
        }else if(type == 'text'){
            return false;
        }
    }

    async getImageFromMessage(client, message){
        var promise = client.downloadMedia(message.id);
        // var options = this.options;
        var chat = this;
        await promise.then(function(val){
            chat.setMessage(val);
            let base64 = {
                img: val
            };
            base64 = JSON.stringify(base64);
            fs.writeFile('tokens/base64.json', base64, 'utf8', function(errfs, resfs){
                if(errfs) 
                    throw errfs; 
                else 
                    pyshell.PythonShell.run("controllers/misc.py", chat.options, function(err, res){ if(err) throw err; else console.log(res); });
            });
            // chat.options.args.push(val)
        }).catch(function(err){
            console.log(err)
        });
    }

    // splitEncode(encode){
    //     let len = (encode.length);
    //     this.options.args = [encode.slice(0, (len/4)), encode.slice((len/4), (len/2)), encode.slice((len/2), (len - (len/4))), encode.slice((len - (len/4)), len)]
    //     console.log(this.options.args)
    // }

}