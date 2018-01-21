import $ from 'jquery';

$('#annotations-container').on('click', 'button.btn-delete', function () {
  const $row = $(this).closest('tr');
  $row.hide('slow', function () { $row.remove(); });
});
