/// Piano scripts
const keys = document.querySelectorAll('.key');
const whiteKeys = document.querySelectorAll('.key.white');
const blackKeys = document.querySelectorAll('.key.black');

const WHITE_KEYS = ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'q', 'w', 'e', 'r', 't', 'y', 'u'];
const BLACK_KEYS = ['s', 'd', 'g', 'h', 'j', '2', '3', '5', '6', '7'];
const NOTES = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab'];

let notesPlayed = [];
const noteHistory = document.getElementById('note-history');
const maxNotes = 6;

function arrToString(arr) {
    let res = '';
    for (let i = 0; i < arr.length; i++) {
        res = res.concat(arr[i]);
        res = res.concat(' ');
    }
    return res;
}

keys.forEach(key => {
    key.addEventListener('click', () => playNote(key));
});

const helpText = document.getElementsByClassName('help-text');

function toggleHelp() {
    for (let i = 0; i < helpText.length; i++) {
        helpText[i].classList.toggle('inactive');
    }
}
toggleHelp();

const helpButton = document.getElementById('help-button');
helpButton.addEventListener('click', () => toggleHelp());

function playNote(key) {
    const noteAudio = document.getElementById(key.dataset.note);
    noteAudio.currentTime = 0;
    noteAudio.play();
    key.classList.add('active');
    noteAudio.addEventListener('ended', () => {
        key.classList.remove('active');
    });
    /// add note to notesPlayed array and display the changes on screen
    const noteName = key.dataset.note;
    if (notesPlayed.length === maxNotes) {
        notesPlayed = notesPlayed.slice(1);
    }
    notesPlayed.push(noteName);
    noteHistory.innerHTML = "Notes played: ".concat(arrToString(notesPlayed));
}

document.addEventListener('keydown', e => {
    if (e.repeat) return;
    const key = e.key;
    const whiteKeyIndex = WHITE_KEYS.indexOf(key);
    const blackKeyIndex = BLACK_KEYS.indexOf(key);
    if (whiteKeyIndex > -1) playNote(whiteKeys[whiteKeyIndex]);
    if (blackKeyIndex > -1) playNote(blackKeys[blackKeyIndex]);
});

/// Chord matching game scripts
const startButton = document.getElementById('start-button');
const endButton = document.getElementById('end-button');
const checkButton = document.getElementById('check-button');
const timer = document.getElementById('timer');
const startText = document.querySelectorAll('.start-text');
const requestedChordText = document.getElementById('requested-chord');
const roundTime = 60;

let state = undefined;
let t = roundTime;
let requestedChord = undefined;
startButton.addEventListener('click', () => startGame());
endButton.addEventListener('click', function() {
    state = 'stopped';
});
checkButton.addEventListener('click', function() {
    t = -1;
});
document.addEventListener('keyup', e => {
    if (e.code === 'Space') {
        t = -1;
    }
});

function generateRandomChord() {
    let rootIdx = Math.floor(Math.random() * 12);
    let chordName = ''.concat(NOTES[rootIdx]);
    let third = Math.random();
    if (third <= 0.5) {
        third = NOTES[(rootIdx + 4) % 12];
    }
    else {
        third = NOTES[(rootIdx + 3) % 12];
        chordName = chordName.concat('min');
    }
    let seven = Math.random();
    if (seven <= 0.5) {
        seven = NOTES[rootIdx - 1];
        chordName = chordName.concat('Maj7');
    }
    else {
        seven = NOTES[rootIdx - 2];
        chordName = chordName.concat('7');
    }
    /// can remove or add notes here, be sure to remove them from the chordName too
    return [chordName, NOTES[rootIdx], third, NOTES[(rootIdx + 7) % 12], seven];
}

function toggleButtons() {
    startButton.classList.toggle('inactive');
    startText.forEach(paragraph => {
        paragraph.classList.toggle('inactive');
    });
    endButton.classList.toggle('inactive');
    checkButton.classList.toggle('inactive');
    timer.classList.toggle('inactive');
    noteHistory.classList.toggle('inactive');
    requestedChordText.classList.toggle('inactive');
}

function resetVariables() {
    t = roundTime;
    notesPlayed = [];
    noteHistory.innerHTML = "Notes played: ";
    requestedChord = generateRandomChord();
    requestedChordText.innerHTML = "Requested chord: ".concat(requestedChord[0]);
}

function checkChord() {
    let requestedNotes = requestedChord.slice(1);
    let playedNotes = [];
    for (let i = notesPlayed.length - 1; i >= notesPlayed.length - requestedNotes.length && i >= 0; i--) {
        playedNotes.push(notesPlayed[i].slice(0, -1));
    }
    if (requestedNotes.length != playedNotes.length) {
        return false;
    }
    requestedNotes.sort();
    playedNotes.sort();
    let flag = true;
    for (let i = 0; i < requestedNotes.length && flag === true; i++) {
        if (requestedNotes[i] !== playedNotes[i]) {
            flag = false;
        }
    }
    return flag;
}

function startGame() {
    state = 'running';
    resetVariables();
    toggleButtons();
    let timerInterval = setInterval(function() {
        if (t !== -1) {
            timer.innerHTML = t.toString(10);
            t--;
        }
        if (t === -1) {
            if (checkChord() === true) {
                /* add to account points */
                Swal.fire('Good job!', 'You played the correct chord.', 'success');
                const userId = window.localStorage.getItem('loggedin');
                if (userId !== null) {
                    const user = JSON.parse(window.localStorage.getItem("user".concat(userId)));
                    user.points = parseInt(user.points) + 1;
                    window.localStorage.setItem("user".concat(userId), JSON.stringify(user));
                }
            }
            else {
                Swal.fire({
                    icon: 'error',
                    title: 'Wrong!',
                    text: 'The chord you played was not the requested chord.'
                });
            }
            resetVariables();
        }
        if (state === 'stopped') {
            clearInterval(timerInterval);
            toggleButtons();
        }
    }, 1000);
}