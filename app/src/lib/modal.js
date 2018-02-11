import $ from 'jquery';

const modalTemplate = require('../templates/annotation-popup.handlebars');
const rowTemplate = require('../templates/annotation-row.handlebars');

function createModal(startId, endId) {
  const html = modalTemplate({
    startId,
    endId,
  });


  const $old = global.annotationMap.get(`${startId}:${endId}`);

  const element = document.getElementById('annotation-popup');

  element.innerHTML = html;

  const modal = $('#annotation-modal');
  modal.modal();

  const submitButton = $('#annotation-modal button[type="submit"]');
  submitButton.prop('disabled', true);

  // Check if pair is already annotated and pre-select
  if ($old !== undefined) {
    const oldRelationship = $old.row.find('select').val();
    modal.find(`.card[data-value='${oldRelationship}']`).addClass('selected');
    submitButton.prop('disabled', false);
  }

  $('#annotation-modal .card').click(function () {
    $('#annotation-modal .card').removeClass('selected');
    $(this).addClass('selected');
    submitButton.prop('disabled', false);
  });

  submitButton.click(function () {
    // TODO Write hidden inputs too
    const relationship = modal.find('.card.selected').data('value');

    modal.modal('hide');

    if ($old !== undefined) {
      // Update old row in DOM
      $old.row.find('select').val(relationship);
      global.annotationMap = global.annotationMap.set(`${startId}:${endId}`, {
        row: $old.row,
      });
      return;
    }

    const $row = $(rowTemplate({
      startId,
      endId,
      relationship,
    }));

    // Set the selected option as active
    $row.find('select').val(relationship);

    $row.prependTo('#annotations-container tbody');

    global.annotationMap = global.annotationMap.set(`${startId}:${endId}`, {
      row: $row,
    });
  });
}

export default createModal;
