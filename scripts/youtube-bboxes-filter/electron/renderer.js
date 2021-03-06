const Papa = require('papaparse');
const fs = require("fs");
const _ = require('lodash');
const {Set} = require('immutable')

const $video = $('#video');
const $annotations = $('#annotations');

let toReviewStream = fs.createReadStream('../videos_with_cars.csv');
let annotationsStream = fs.createReadStream('../videos_with_cars_annotations.csv');
let reviewedVideosStream = fs.createReadStream('reviewedVideos.csv');

let videos = [];
let reviewedVideos = null;
let annotations = null;
let currentVideo = 0;

function loadData() {
    return new Promise((resolve, reject) => {
        Papa.parse(toReviewStream, {
        complete: function (results) {
            videos = results.data;
            $('#video-total').html(videos.length);
            resolve();
        },
        header: true
    });
}).
    then(() => {
        return new Promise((resolve, reject) => {
            Papa.parse(annotationsStream, {
            complete: function (results) {
                annotations = _.groupBy(results.data, 'youtube_id');
                resolve();
            },
            header: true
        });
})
    ;
}).
    then(() => {
        return new Promise((resolve, reject) => {
            Papa.parse(reviewedVideosStream, {
            complete: function (results) {
                let ids = _.map(results.data, 'youtube_id');
                reviewedVideos = Set(ids);
                resolve();
            },
            header: true
        });
})
    ;
})
    ;
}

loadData().then(() => {
    setVideo(0
)
;
$('button').prop('disabled', false);

//Poll YouTube timer
setInterval(function () {
    let timestamp = player.getCurrentTime();

    if (timestamp === undefined) return;

    let endTime = $('input[name="end"]').val();

    if (endTime !== "") {
        endTime = parseFloat(endTime);
        if (timestamp > endTime) player.pauseVideo();
    }

    timestamp = timestamp.toFixed(2);
    $('#current-time').html(timestamp);
}, 100)
})
;

$('#btn-yes').click(function () {
    const videoId = $video.data('video-id');
    console.log('Approving', videoId);
    writeWideo(videoId, 1);

    nextVideo();
});

$('#btn-no').click(function () {
    const videoId = $video.data('video-id');
    writeWideo(videoId, 0);
    nextVideo();
});

$('#btn-video-go').click(function () {
    const videoNo = $('#input-video').val()
    setVideo(parseInt(videoNo));
});

$('#btn-youtube-id').click(function () {
    const youtubeId = $('#input-youtube-id').val()
    setVideoById(youtubeId);
});

$('button.btn-set-time').click(function () {
    let timestamp = player.getCurrentTime();
    console.log('setting to', timestamp);
    let $input = $(this).closest('div.input-group').find('input');
    $input.val(timestamp);

    let name = $input.attr('name');

    if (name == 'start') {
        $('input[name="end"]').val(timestamp + 5);
    }
});

function nextVideo() {
    currentVideo++;

    setVideo(currentVideo)
}

function isVideoReviewed(videoId) {
    return reviewedVideos.has(videoId);
}

function setVideo(videoNo) {
    currentVideo = videoNo;

    if (videoNo >= videos.length) {
        alert('No more videos to review');
        return;
    }

    const vid = videos[videoNo];

    const videoId = vid['youtube_id'];

    if (isVideoReviewed(videoId)) {
        console.log("Skipping", videoId);
        nextVideo();
        return;
    }

    $('#video-current').html(currentVideo);

    setVideoById(videoId);
}

function setVideoById(youtubeId) {
    // Update iframe
    $video.data('video-id', youtubeId);

    player.loadVideoById(youtubeId);
    $('#video-url').html(`https://www.youtube.com/watch?v=${youtubeId}`);

    $annotations.find('tbody').empty();

    $('input[name="start"]').val("");
    $('input[name="end"]').val("");

    if (annotations[youtubeId] === undefined) {
        return;
    }

    for (let row of annotations[youtubeId]) {
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
