const express = require('express');
const router = express.Router();
const Post = require('../models/post');

router.get('/', async (req, res) => {
	
	try {
		
		res.send('Nothing to see here');

	} catch (err) {
		res.status(500).json({ "error": err.message });
	}

});

router.post('/', async (req, res) => {
	
	try {
		// Prometheus
		temp.set(req.body.temperature); // Set to 10

		// MongoDB
		const post = new Post({
			date: req.body.date,
			temperature: req.body.temperature,
			plants: req.body.plants
		});

		const savedPost = await post.save();

		res.status(200).json(savedPost);

	} catch (err) {
		res.status(500).json({ "error": err.message });
	}

});

// Prometheus metrics endpoint
router.get('/metrics', async(req, res) => {

	try {

		res.set('Content-Type', client.register.contentType);
		res.end(client.register.metrics());

	} catch (err) {
		res.status(500).json({ "error": err.message });
	}
});

module.exports = router;