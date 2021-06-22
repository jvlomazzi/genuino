const mongoose = require("mongoose");

mongoose.connect('mongodb://localhost/genuino', { useMongoClient: true });
mongoose.Promise = global.Promise;

module.exports = mongoose;