import createModal from './modal';

const video = document.getElementById('video');
const canvas = document.getElementById('overlay');
let lastTime = -1;
let videoData;
let scaleFactor;
let BoundingBoxes = [];

// Create a stage by getting a reference to the canvas
const stage = new createjs.Stage('overlay');
stage.enableMouseOver();

/* FIXME
canvas.onclick = function(e) {
    players[0].togglePlay();
};
*/

video.onplay = () => {
  const w = video.offsetWidth;
  const h = video.offsetHeight;

  // TODO On resize, the scale factor will probably break

  scaleFactor = w / videoData.width;

  canvas.width = w;
  canvas.height = h;
};


function hitTestBBox(stageX, stageY) {
  for (const box of BoundingBoxes) {
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
});

stage.on('stagemousemove', (evt) => {
  if (!dragSelect.dragging) return;

  dragSelect.line.graphics.clear();
  dragSelect.line.graphics
    .setStrokeStyle(3)
    .beginStroke('#0000FF')
    .moveTo(dragSelect.startPoint.stageX, dragSelect.startPoint.stageY)
    .lineTo(evt.stageX, evt.stageY)
    .endStroke();

  // TODO: Add overlay on hovering

  stage.update();
});

stage.on('stagemouseup', (evt) => {
  const hitId = hitTestBBox(evt.stageX, evt.stageY);
  console.log(`Start: ${dragSelect.startId} End ID: ${hitId}`);
  dragSelect.dragging = false;

  // TODO: Ignore accidental clicks
  // TODO: Ignore identical start and ends

  createModal(dragSelect.startId, hitId);
});

function drawFrame(frameNumber) {
  const bboxes = videoData.annotations[frameNumber];

  stage.removeAllChildren();

  if (bboxes === undefined) {
    console.warn('Bboxes undefined frame number', frameNumber);
    return;
  }

  BoundingBoxes = [];

  bboxes.forEach((box) => {
    const entityId = box[0];
    const rect = new createjs.Shape();
    const x = box[1] * scaleFactor;
    const y = box[2] * scaleFactor;
    const width = box[3] * scaleFactor;
    const height = box[4] * scaleFactor;
    rect.graphics.beginStroke('red').drawRect(
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

    const label = new createjs.Text(`ID: ${entityId}`, '48px Arial', '#42f442');
    label.x = x;
    label.y = y - 10;
    label.visible = false;
    stage.addChild(label);

    rect.on('mouseover', () => {
      label.visible = true;
      stage.update();

      setTimeout(() => {
        label.visible = false;
        stage.update();
      }, 3000);
    });

    rect.on('mouseout', () => {
      label.visible = false;
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

  // TODO: Sort by area of rectangle for z-level

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
  videoData = data;
  draw();
}

export {
  startDrawingOverlay,
};
