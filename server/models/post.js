const mongoose = require('mongoose');

const PostSchema = mongoose.Schema({
    date: {
        type: Date,
        required: true,
        default: Date.now
    },
    moisture: [{
        type: Boolean, 
        required: true
    }]
});


module.exports = mongoose.model('post', PostSchema);