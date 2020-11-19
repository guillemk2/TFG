const express = require('express');
const router = express.Router();
const Post = require('../models/post');

router.get('/', async (req, res) => {
	
	try {
		
		res.send('Get some info');

	} catch (err) {
		res.status(500).json({ "error": err.message });
	}

});

router.post('/', async (req, res) => {
	
	try {

		const post = new Post({
			date: req.body.date,
			moisture: req.body.moisture
		});

		const savedPost = await post.save();

		res.status(200).json(savedPost);

	} catch (err) {
		res.status(500).json({ "error": err.message });
	}

});

module.exports = router;