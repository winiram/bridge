$(document).ready(function() {
    $('select').material_select();
    $('#customSearchOptions').hide();
    $('#customizeSearch').click(function() {
        $('#customSearchOptions').toggle();
    });
    // $("#addButton").click(function () {
    //     clone_field_list('fieldset:last');
    // });

    function addRow() {
      console.log("Adding row")
      var url='/createSearch'
      $.post(
        url,
        {
          action:"add"
        }
      );
    }
});

function clone_field_list(selector) {
  var new_element = $(selector).clone(true);
  var elem_id = new_element.find(':input')[0].id;
  var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
  new_element.find(':input').each(function() {
      var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
      $(this).attr({'name': id, 'id': id}).val('').removeAttr('checked');
  });
  new_element.find('label').each(function() {
      var new_for = $(this).attr('for').replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
      $(this).attr('for', new_for);
  });
  $(selector).after(new_element);
}
