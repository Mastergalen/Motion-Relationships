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
$('#videoId').val(youtubeId);
const submitUrl = `${qs('turkSubmitTo')}/mturk/externalSubmit`;
$('#mturk_form').attr('action', submitUrl);

const videoDir = `videos/${youtubeId}`;

$('#video source').attr('src', `${videoDir}.mp4`);

plyr.setup();
global.annotationMap = Map();

fetch(`${videoDir}.json`).then(res => res.json()).then((json) => {
  const videoData = json;
  startDrawingOverlay(videoData);

  $('#video-container').removeClass('loading');
});

