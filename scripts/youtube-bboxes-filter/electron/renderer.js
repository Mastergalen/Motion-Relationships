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
  setVideo(0);
  $('button').prop('disabled', false);  

  //Poll YouTube timer
  setInterval(function() {
    let timestamp = player.getCurrentTime();

    if(timestamp === undefined) return;

    let endTime = $('input[name="end"]').val();

    if(endTime !== "") {
      endTime = parseFloat(endTime);
      if(timestamp > endTime) player.pauseVideo();
    }

    timestamp = timestamp.toFixed(2);
    $('#current-time').html(timestamp);
  }, 100)
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

$('#btn-video-go').click(function() {
  const videoNo = $('#input-video').val()
  setVideo(parseInt(videoNo));
});

$('button.btn-set-time').click(function() {
  let timestamp = player.getCurrentTime();
  console.log('setting to', timestamp);
  let $input = $(this).closest('div.input-group').find('input');
  $input.val(timestamp);

  let name = $input.attr('name');

  if(name == 'start') {
    $('input[name="end"]').val(timestamp + 5);
  }
});

function nextVideo() {
  currentVideo++;

  setVideo(currentVideo)
}

function setVideo(videoNo) {
  currentVideo = videoNo;
  const vid = videos[videoNo];
  $('#video-current').html(currentVideo);

  const videoId = vid['youtube_id'];
  // Update iframe
  $video.data('video-id', videoId);
  
  player.loadVideoById(videoId);
  $('#video-url').html(`https://www.youtube.com/watch?v=${videoId}`);

  $annotations.find('tbody').empty();

  $('input[name="start"]').val("");
  $('input[name="end"]').val("");

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
  let start = $('input[name="start"]').val();
  let end = $('input[name="end"]').val();

  fs.appendFileSync('reviewedVideos.csv', `${videoId},${status},${currentVideo},${classesInVideo.join('|')},${new Date().toISOString()},${start},${end}\n`);
}