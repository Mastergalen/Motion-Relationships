import { startDrawingOverlay } from './lib/overlay';

const players = plyr.setup();

document.body.onkeyup = (e) => {
  if (e.keyCode === 32) {
    players[0].togglePlay();
    e.preventDefault();
  }
};

fetch('https://s3.amazonaws.com/amt-motion-relationships/videos/MOT17-09-DPM.json').then(res => res.json()).then((json) => {
  const videoData = json;
  startDrawingOverlay(videoData);
});
