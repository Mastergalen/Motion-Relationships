import $ from 'jquery';

$('#annotations-container').on('click', 'button.btn-delete', function () {
  const $row = $(this).closest('tr');

  // Delete entry from annotationMap
  const startId = $row.children('td').first().html().trim();
  const endId = $row.children('td').eq(1).html().trim();
  global.annotationMap = global.annotationMap.delete(`${startId}:${endId}`);

  $row.hide('slow', function () { $row.remove(); });
});
