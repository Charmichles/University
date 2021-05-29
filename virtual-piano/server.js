const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');
const port = 3000;
const uid = require('uid');

const DISLIKES_MAX = 4;
let comments = []

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
/// pentru a avea acces la fisierele de css si js
app.use(express.static(__dirname + '/public'));

app.get('/index.html', (req, res) => {
    res.sendFile(__dirname + '/public/pages/index.html');
    res.status(200);
});

app.get('/learn.html', (req, res) => {
    res.sendFile(__dirname + '/public/pages/learn.html');
    res.status(200);
});

app.get('/login.html', (req, res) => {
    res.sendFile(__dirname + '/public/pages/login.html');
    res.status(200);
});

app.get('/lista-comments', (req, res) => {
    res.send(comments);
});

app.post('/adauga-comment', (req, res) => {
    const commentData = req.body;
    commentData.id = uid(32);
    comments.push(req.body);
    res.statusCode = 201;
    res.send(comments);
});

app.post('/like-comment', (req, res) => {
    const comment_id = req.body.id;
    for (let i = 0; i < comments.length; i++) {
        if (comments[i].id === comment_id) {
            comments[i].likes = String(parseInt(comments[i].likes) + 1);
            break;
        }
    }
    res.statusCode = 200;
    res.send(comments);
});

app.post('/dislike-comment', (req, res) => {
    const comment_id = req.body.id;
    for (let i = 0; i < comments.length; i++) {
        if (comments[i].id === comment_id) {
            comments[i].dislikes = String(parseInt(comments[i].dislikes) + 1);
            if (parseInt(comments[i].dislikes) >= DISLIKES_MAX) {
                comments[i].state = 'inactive';
            }
            break;
        }
    }
    res.statusCode = 200;
    res.send(comments);
});

app.get('*', (req, res) => {
    res.sendFile(__dirname + '/public/pages/error.html');
    res.status(404);
});

app.listen(port);