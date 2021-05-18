const pyshell = require('python-shell');
const fs = require('fs');
module.exports = class Chatbot {
    apresentacao = 'Olá eu sou o *Genuíno* 👴, um robô criado para te auxiliar na checagem de fatos.\n\n' +
    '📰 Basta você me enviar uma notícia e eu direi se ela é falsa ou não.\n' +
    '🟢 Consigo ler mensagens através de capturas de tela (do título da notícia) e também por texto.\n\n' +
    'Quer saber como enviar uma notícia para avaliação? Envie *ajuda* que eu te mostro!';
    
    message;

    route = "config/routes.py";
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

    
    verifyMessage(client, message) {
        let type = message.type;
        let body = message.body;
        console.log(type)
        switch(type){
            case 'chat':
                this.getTextData(client, body)
                break;
            case 'image':
                this.sendImageToServer(client, message);
                break;
            default:
                console.log("Tipo invalido de mensagem.")
                break;
        }
    }

    getTextData(client, body){
        console.log("start ------ getTextData");
        //é url - enviar para backend fazer a predição de dados
        //precisa enviar apresentacao
        //precisa de ajuda - enviar para backend chatterbot
        if(this.validURL(body)){
            console.log("É url");
            this.setServerArgs('url');
            this.setServerArgs(body);
            this.sendToServer();
        }else{
            console.log("Não é url");
        }
    }

    validURL(str) {
        var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
          '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
          '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
          '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
          '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
          '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
        return !!pattern.test(str);
      }
    /**
     * Verifica se é uma mensagem de resposta imediata, como por exemplo "Olá", "Ajude-me".
     * Mensagens de respostas NÃO imediatas podem ser enviadas seguidas de um link, fazendo com que o chatbot pule uma etapa.
     */
    // isImmediateAnswer(){

    // }

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

    async sendImageToServer(client, message){
        var promise = client.downloadMedia(message.id);
        var chat = this;
        await promise.then(function(val){
            chat.setMessage(val);
            let base64 = {
                img: val
            };
            base64 = JSON.stringify(base64);
            fs.writeFile('tokens/base64.json', base64, 'utf8', function(errfs, resfs){
                if(errfs){ 
                    throw errfs; 
                }else{
                    this.setServerArgs('image');
                    this.sendToServer();
                }
            });
        }).catch(function(err){
            console.log(err)
        });
    }

    async sendToServer(){
        pyshell.PythonShell.run(this.route, this.options, function(err, res){ if(err) throw err; else console.log(res); });
    }

}