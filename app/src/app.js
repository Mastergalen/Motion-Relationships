import 'bootstrap';
import $ from 'jquery';
import { Map } from 'immutable';
import './scss/main.scss';
import { startDrawingOverlay } from './lib/overlay';
import './lib/annotations-table';

/**
 * Get the query string parameter
 * @param {string} key
 */
function qs(key) {
  const escapedKey = key.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
  const match = location.search.match(new RegExp("[?&]"+escapedKey+"=([^&]+)(&|$)"));
  return match && decodeURIComponent(match[1].replace(/\+/g, " "));
}

const youtubeId = qs('video');

if (youtubeId === null) {
  console.error('?video= parameter not set');
  alert('Video parameter not set');
}

$('#assignmentId').val(qs('assignmentId'));
const submitUrl = `${qs('turkSubmitTo')}/mturk/externalSubmit`;
$('#mturk_form').attr('action', submitUrl);

const videoDir = `videos/${youtubeId}`;

$('#video source').attr('src', `${videoDir}.mp4`);

const players = plyr.setup();
global.annotationMap = Map();

document.body.onkeydown = (e) => {
  if (e.keyCode === 32) {
    e.preventDefault();
  }
};

document.body.onkeyup = (e) => {
  if (e.keyCode === 32) {
    players[0].togglePlay();
    e.preventDefault();
  }
};

// TODO Do not enable play button until videoData is loaded

fetch(`${videoDir}.json`).then(res => res.json()).then((json) => {
  const videoData = json;
  startDrawingOverlay(videoData);
});

