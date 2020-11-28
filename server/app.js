const express = require('express');
const mongoose = require('mongoose');
require("dotenv").config({ path: '/home/pi/Documents/.env' }); 
const app = express();

// DB connection
mongoose.set('useUnifiedTopology', true);
mongoose.set('useCreateIndex', true);

mongoose.connect(process.env.DB_CONNECTION, { useNewUrlParser: true, useUnifiedTopology: true })
.then(db => console.log('DB connected.'))
.catch(err => console.log('DB error: ', err.message));

// Middlewares I
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

//ROUTES
app.use('/', require('./routes/routes'));

// Settings
app.set('httpPort', process.env.HTTPPORT || 8080);

//Listen
app.listen(app.get('httpPort'), () => {
    console.log(`HTTP server on port ${app.get('httpPort')}`);
});
