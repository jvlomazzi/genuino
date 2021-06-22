const mongoose = require('mongoose');

const MessageSchema = new mongoose.Schema({
    mensagem: {
        type: String,
        require: true
    }
});

const Message = mongoose.model('Message', MessageSchema);