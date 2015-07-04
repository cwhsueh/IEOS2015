var mongoose = require('mongoose');

var deviceSchema = mongoose.Schema({
    device_name : String,
    ip_adress   : String,
    actions     : Array
});

module.exports = mongoose.model('Device', deviceSchema);