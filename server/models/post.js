const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const PostSchema = Schema({
	date: {
		type: Date,
		required: true,
		default: Date.now
	},
	temperature: {
		type: Schema.Types.Decimal128,
		required: true
	},
	plants: [{
		moisture: {
			type: Number, 
			required: true
		},
		irrigation: {
			type: Schema.Types.Decimal128,
			required: true
		}
	}]
});


module.exports = mongoose.model('post', PostSchema);