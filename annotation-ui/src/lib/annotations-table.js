import $ from 'jquery';
import _ from 'lodash';

$('#annotations-container').on('click', 'button.btn-delete', function () {
  const $row = $(this).closest('tr');

  // Delete entry from annotationMap
  const startId = $row.children('td').first().html().trim();
  const endId = $row.children('td').eq(1).html().trim();
  global.annotationMap = global.annotationMap.delete(`${startId}:${endId}`);

  $row.hide('slow', function () { $row.remove(); });
});

$('#mturk_form').submit(function (e) {
  const formData = $(this).serializeArray();
  const relationshipAnnotations = _.filter(formData, function (o) {
    return o.name.substring(0, 13) === 'relationship-';
  });
  if (relationshipAnnotations.length === 0) {
    if (!window.confirm('You annotated zero relationships, submit anyway?')) {
      e.preventDefault();
    }
  }
});
