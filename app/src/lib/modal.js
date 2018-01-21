import $ from 'jquery';

const modalTemplate = require('../templates/annotation-popup.handlebars');
const rowTemplate = require('../templates/annotation-row.handlebars');

function createModal(startId, endId) {
  const html = modalTemplate({
    startId,
    endId,
  });

  // TODO: Check if pair already annotated and pre-select

  const element = document.getElementById('annotation-popup');

  element.innerHTML = html;

  const modal = $('#annotation-modal');
  modal.modal();

  const submitButton = $('#annotation-modal button[type="submit"]');
  submitButton.prop('disabled', true);

  $('#annotation-modal .card').click(function () {
    $('#annotation-modal .card').removeClass('selected');
    $(this).addClass('selected');
    submitButton.prop('disabled', false);
  });

  submitButton.click(function () {
    // TODO Write hidden inputs too
    const relationship = modal.find('.card.selected').data('value');

    modal.modal('hide');

    const rowHtml = rowTemplate({
      startId,
      endId,
      relationship,
    });

    $('#annotations-container tbody').append(rowHtml);
  });
}

export default createModal;
