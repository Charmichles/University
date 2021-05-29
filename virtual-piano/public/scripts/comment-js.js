const commentBox = document.getElementById('comments');
const postButton = document.getElementById('post-button');
const toggleButton = document.getElementById('comment-toggle-button');
const myForm = document.getElementById('myform');

if (window.localStorage.getItem('loggedin') !== null) {
    const userId = window.localStorage.getItem('loggedin');
    const userObj = JSON.parse(window.localStorage.getItem('user'.concat(userId)));
    myForm.elements["comment-username"].value = userObj.username;
    myForm.elements["comment-username"].readOnly = true;
}

async function initComments() {
    const comms = await getData('http://localhost:3000/lista-comments');
    showComments(comms);
}

toggleButton.addEventListener('click', function() {
    commentBox.classList.toggle('inactive');
    myForm.classList.toggle('inactive');
});

async function showComments(commentsList) {
    commentBox.innerHTML = '';
    commentsList.forEach(comment => {
        const tempComment = `
        <div class = "comment" data-id = ${comment.id}>
            <span class = "username">Comment from: ${comment.username}</span>
            <span class = "comment-content ${comment.state}">${comment.commentBody}</span>
            <span class = "hidden-text ${comment.state}">This comment was deleted because of too many dislikes.</span>
            <div class = "rating-wrapper ${comment.state}">
                <button class = "rating-button" data-id = ${comment.id} onclick = "likeComment(this)">Likes: ${comment.likes}</button>
                <button class = "rating-button" data-id = ${comment.id} onclick = "dislikeComment(this)">Dislikes: ${comment.dislikes}</button>
            </div>
        </div>
        `
        commentBox.insertAdjacentHTML("beforeend", tempComment);
    });
}

async function getData(url = '') {
    const response = await fetch(url);
    return response.json();
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
       method: 'POST',
       headers: {
           'Accept': 'application/json',
           'Content-Type': 'application/json'
       },
       body: JSON.stringify(data) 
    });
    return response.json();
}

async function addComment() {
    const username = document.getElementById('comment-username').value;
    const commentBody = document.getElementById('comment-body').value;
    const newComment = {
        username,
        commentBody,
        likes: '0',
        dislikes: '0',
        state: ''
    };
    const newCommentList = await postData('http://localhost:3000/adauga-comment', newComment);
    showComments(newCommentList);
}

async function likeComment(comment) {
    const data = {
        id: comment.dataset.id
    };
    const newCommentList = await postData('http://localhost:3000/like-comment', data);
    showComments(newCommentList);
}

async function dislikeComment(comment) {
    const data = {
        id: comment.dataset.id
    };
    const newCommentList = await postData('http://localhost:3000/dislike-comment', data);
    showComments(newCommentList);
}