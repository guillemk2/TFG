const express = require('express');
const router = express.Router();
const Post = require('../models/post');

// Mida del sistema (nombre de testos)
const SYS_SIZE = 2

// Prometheus metrics
const client = require('prom-client');
const collectDefaultMetrics = client.collectDefaultMetrics;
const temp = new client.Gauge({ name: 'temp', help: 'Temperatura ambient' });

var moisture = []
var irrigation = []

for (i = 0; i < SYS_SIZE; i++) {
	moisture.push(new client.Gauge({ name: 'moisture_' + i, help: 'Humitat en test ' + i }));
	irrigation.push(new client.Gauge({ name: 'irrigation_' + i, help: 'Reg en test ' + i }));
}

router.get('/', (req, res) => {
	
	try {
		
		res.send('Nothing to see here');

	} catch (err) {
		res.status(500).json({ "error": err.message });
	}

});

router.post('/', async (req, res) => {
	
	try {
		// Prometheus
		temp.set(req.body.temperature);
		for (i = 0; i < SYS_SIZE; i++) {
			moisture[i].set(req.body.plants[i].moisture);
			irrigation[i].set(req.body.plants[i].irrigation);
		}

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
router.get('/metrics', (req, res) => {

	try {

		res.set('Content-Type', client.register.contentType);
		res.end(client.register.metrics());

	} catch (err) {
		res.status(500).json({ "error": err.message });
	}
});

module.exports = router;