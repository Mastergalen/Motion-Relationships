import $ from 'jquery';

const modalTemplate = require('../templates/annotation-popup.handlebars');
const rowTemplate = require('../templates/annotation-row.handlebars');

function appendRow(startId, endId, relationship) {
  //Check if relationship was previously annotated
  const $container = $('#annotations-container');
  const $select = $container.find(`tbody select[name="relationship-${startId}:${endId}"]`).first();

  if ($select.length > 0) {
    updateSelect(startId, endId, relationship);
    return;
  }

  const $row = $(rowTemplate({
    startId,
    endId,
    relationship,
  }));

  // Set the selected option as active
  $row.find('select').val(relationship);

  $row.prependTo($container.find('tbody'));

  global.annotationMap = global.annotationMap.set(`${startId}:${endId}`, {
    row: $row,
  });
}

function updateSelect(startId, endId, relationship) {
  const $select = $('#annotations-container').find(`tbody select[name="relationship-${startId}:${endId}"]`).first();
  $select.val(relationship);
  const $row = $select.parent('tr');
  global.annotationMap = global.annotationMap.set(`${startId}:${endId}`, {
    row: $row,
  });
}

function createModal(startId, endId) {
  const html = modalTemplate({
    startId,
    endId,
  });

  const $old = global.annotationMap.get(`${startId}:${endId}`);

  const element = document.getElementById('annotation-popup');
  element.innerHTML = html;

  const $modal = $('#annotation-modal');
  $modal.modal();

  const submitButton = $modal.find('button[type="submit"]');
  submitButton.prop('disabled', true);

  // Check if pair is already annotated and pre-select
  if ($old !== undefined) {
    const oldRelationship = $old.row.find('select').val();
    $modal.find(`.card[data-value='${oldRelationship}']`).addClass('selected');
    submitButton.prop('disabled', false);
  }

  const $cards = $modal.find('.card');

  $cards.click(function () {
    $cards.removeClass('selected');
    $(this).addClass('selected');
    submitButton.prop('disabled', false);
  });

  submitButton.click(function () {
    const relationship = $modal.find('.card.selected').data('value');

    $modal.modal('hide');

    appendRow(startId, endId, relationship);

    // Add undirected relationship
    if (relationship === 'group') {
      appendRow(endId, startId, relationship);
    }

    // Set the focus on the player to enable keyboard shortcuts
    $('.plyr.plyr--video').focus();
  });
}

export default createModal;
