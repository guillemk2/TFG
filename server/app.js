const express = require('express');

const app = express();

//ROUTES
app.get('/', (req, res) => {
	res.send('We are on home');
});

//Listen
app.listen(8080);
