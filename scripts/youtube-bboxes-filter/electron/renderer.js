const Papa = require('papaparse');
const fs = require("fs");
const _ = require('lodash');

const $video = $('#video');
const $annotations = $('#annotations');

let stream = fs.createReadStream('../filtered_videos.csv');
let allVideosStream = fs.createReadStream('../multi.csv');

let videos = [];
let annotations = null;
let currentVideo = 0;

function loadData() {
  return new Promise((resolve, reject) => {
    Papa.parse(stream, {
      complete: function(results) {
        videos = results.data;
        $('#video-total').html(videos.length);
        resolve();
      },
      header: true
    });
  }).then(() => {
    return new Promise((resolve, reject) => {
      Papa.parse(allVideosStream, {
        complete: function(results) {
          annotations = _.groupBy(results.data, 'youtube_id');
          resolve();
        },
        header: true
      });
    });
  });
}

loadData().then(() => {
  updateVideo(0);
  $('button').prop('disabled', false);
});

$('#btn-yes').click(function() {
  const videoId = $video.data('video-id');
  console.log('Approving', videoId);
  writeWideo(videoId, 1);

  nextVideo();
});

$('#btn-no').click(function() {
  const videoId = $video.data('video-id');
  writeWideo(videoId, 0);
  nextVideo();
});

function nextVideo() {
  currentVideo++;
  $('#video-current').html(currentVideo);

  updateVideo(currentVideo)
}

function updateVideo(videoNo) {
  const vid = videos[videoNo];

  const videoId = vid['youtube_id'];
  // Update iframe
  $video.data('video-id', videoId);
  
  $video.find('iframe').attr('src', `https://www.youtube.com/embed/${videoId}?autoplay=1`);
  $('#video-url').html(`https://www.youtube.com/watch?v=${videoId}`);

  $annotations.find('tbody').empty();

  for(let row of annotations[videoId]) {
    $annotations.find('tbody').append(`<tr>
      <td>${row['timestamp_ms']}</td>
      <td>${row['class_name']}</td>
    </tr>`);
  }
}

function writeWideo(videoId, status) {
  let classesInVideo = _.map(annotations[videoId], 'class_name');
  classesInVideo = _.uniq(classesInVideo);
  fs.appendFileSync('approvedVideos.csv', `${videoId},${status},${currentVideo},${classesInVideo.join('|')},${new Date().toISOString()}\n`);
}