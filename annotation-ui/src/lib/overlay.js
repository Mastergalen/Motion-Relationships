import $ from 'jquery';
import _ from 'lodash';
import toastr from 'toastr';

import createModal from './modal';

const canvas = document.getElementById('overlay');
let lastTime = -1;
let videoData;
let video;
let scaleFactor;
let BoundingBoxes = [];

// Create a stage by getting a reference to the canvas
const stage = new createjs.Stage('overlay');
stage.enableMouseOver();

function hitTestBBox(stageX, stageY) {
  // Reverse order of BoundingBoxes, to get smallest box first
  for (const box of BoundingBoxes.slice().reverse()) {
    if (stageX >= box.x &&
      stageX <= box.x + box.width &&
      stageY >= box.y &&
      stageY <= box.y + box.height
    ) return box.id;
  }

  return false;
}

const dragSelect = {
  dragging: false,
  startPoint: null,
  startId: null,
  line: new createjs.Shape(),
};
stage.on('stagemousedown', (evt) => {
  dragSelect.dragging = true;
  dragSelect.startPoint = evt;
  const hitId = hitTestBBox(evt.stageX, evt.stageY);

  stage.addChild(dragSelect.line);

  console.log(`Starting ID: ${hitId}`);
  dragSelect.startId = hitId;

  // Set the focus on the player to enable keyboard shortcuts
  $('.plyr.plyr--video').focus();
});

stage.on('stagemousemove', (evt) => {
  if (!dragSelect.dragging) return;

  const arrowLength = 10;
  const arrowAngle = Math.PI / 6;

  const direction = Math.atan2(
    evt.stageY - dragSelect.startPoint.stageY,
    evt.stageX - dragSelect.startPoint.stageX,
  );

  dragSelect.line.graphics.clear();
  dragSelect.line.graphics
    .setStrokeStyle(3)
    .beginStroke('#0000FF')
    .moveTo(dragSelect.startPoint.stageX, dragSelect.startPoint.stageY)
    .lineTo(evt.stageX, evt.stageY)
    // Draw arrow head
    .lineTo(
      evt.stageX - (arrowLength * Math.cos(direction - arrowAngle)),
      evt.stageY - (arrowLength * Math.sin(direction - arrowAngle)),
    )
    .moveTo(evt.stageX, evt.stageY)
    .lineTo(
      evt.stageX - (arrowLength * Math.cos(direction + arrowAngle)),
      evt.stageY - (arrowLength * Math.sin(direction + arrowAngle)),
    )
    .endStroke();

  stage.update();
});

stage.on('stagemouseup', (evt) => {
  const hitId = hitTestBBox(evt.stageX, evt.stageY);
  dragSelect.dragging = false;

  const dragDistance = Math.sqrt(((dragSelect.startPoint.stageX - evt.stageX) ** 2) +
  ((dragSelect.startPoint.stageY - evt.stageY) ** 2));

  // Remove line
  dragSelect.line.graphics.clear();
  stage.update();

  // Ignore accidental clicks
  if (dragDistance < 1.0) return;

  console.log(`Start: ${dragSelect.startId} End ID: ${hitId}`);

  if (dragSelect.startId === false || hitId === false) {
    toastr.error('Oops, looks like you did not draw a line between two objects which are in a red box.');
    return;
  }

  // Ignore identical start and ends
  if (dragSelect.startId === hitId) {
    toastr.error('No need to annotate the relationship with itself, instead try drawing a line betwen two different objects in red boxes.');
    return;
  }

  createModal(dragSelect.startId, hitId);
});

function drawFrame(frameNumber) {
  let bboxes = videoData.annotations[frameNumber];

  stage.removeAllChildren();

  if (bboxes === undefined) {
    if (frameNumber > 0) {
      drawFrame(frameNumber - 1);
    } else {
      console.warn('Bboxes undefined frame number', frameNumber);
    }
    return;
  }

  BoundingBoxes = [];

  // Sort by area of rectangle to minimise occlusion
  bboxes = _.reverse(_.sortBy(bboxes, el => el[3] * el[4]));

  bboxes.forEach((box) => {
    const entityId = box[0];
    const rect = new createjs.Shape();
    const x = box[1] * scaleFactor;
    const y = box[2] * scaleFactor;
    const width = box[3] * scaleFactor;
    const height = box[4] * scaleFactor;
    const strokeCmd = rect.graphics.setStrokeStyle(1).command;
    const colourCmd = rect.graphics.beginStroke('red').command;
    rect.graphics.drawRect(
      x,
      y,
      width,
      height,
    );
    const hit = new createjs.Shape();
    hit.graphics.beginFill('#000').rect(
      x,
      y,
      width,
      height,
    );
    rect.hitArea = hit;
    stage.addChild(rect);

    const label = new createjs.Text(`ID: ${entityId}`, '40px Arial', '#42f442');
    label.x = x;
    label.y = y - 10;
    label.visible = false;
    stage.addChild(label);

    rect.on('mouseover', function () {
      label.visible = true;
      strokeCmd.width = 3;
      colourCmd.style = 'blue';
      stage.update();

      setTimeout(() => {
        label.visible = false;
        stage.update();
      }, 3000);
    });

    rect.on('mouseout', () => {
      label.visible = false;
      strokeCmd.width = 1;
      colourCmd.style = 'red';
      stage.update();
    });

    BoundingBoxes.push({
      x,
      y,
      width,
      height,
      id: entityId,
    });
  });

  stage.update();
}

function draw() {
  const time = video.currentTime;
  if (time !== lastTime) {
    const frame = Math.floor(time * videoData.frameRate);

    drawFrame(frame);

    lastTime = time;
  }

  // wait approximately 16ms and run again
  requestAnimationFrame(draw);
}

function startDrawingOverlay(data) {
  video = global.player.getMedia();

  global.player.on('play', function () {
    const w = video.offsetWidth;
    const h = video.offsetHeight;
  
    scaleFactor = w / videoData.width;
  
    canvas.width = w;
    canvas.height = h;
  });

  videoData = data;
  draw();
}

export {
  startDrawingOverlay,
};
