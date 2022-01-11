const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');
const port = 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
/// pentru a avea acces la fisierele de css si js
app.use(express.static(__dirname + '/public'));

app.get('/index.html', (req, res) => {
    res.sendFile(__dirname + '/public/pages/index.html');
    res.status(200);
});

app.get('*', (req, res) => {
    res.sendFile(__dirname + '/public/pages/error.html');
    res.status(404);
});

app.listen(port);