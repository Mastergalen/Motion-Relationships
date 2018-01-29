import 'bootstrap';
import './scss/main.scss';
import { startDrawingOverlay } from './lib/overlay';
import './lib/annotations-table';

const players = plyr.setup();

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

fetch('https://s3.amazonaws.com/amt-motion-relationships/videos/-3K26M-m_00.json').then(res => res.json()).then((json) => {
  const videoData = json;
  startDrawingOverlay(videoData);
});
