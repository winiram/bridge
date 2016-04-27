$(document).ready(function() {
    $('select').material_select();
    $('#customSearchOptions').hide();
    $('#customizeSearch').click(function() {
        $('#customSearchOptions').toggle();
    });
    $("#addButton").click(function () {
        clone_field_list('div[class*=searchField]');
    });

    // function addRow() {
    //   console.log("Adding row")
    //   var url='/createSearch'
    //   $.post(
    //     url,
    //     {
    //       action:"add"
    //     }
    //   );
    // }
});

function clone_field_list(selector) {
  var new_element = $(selector).last().clone(true);
  console.log($(selector).last());
  var elem_id = new_element.find('input')[0].id;
  console.log(elem_id);
  var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
  console.log(elem_num);
  console.log(new_element.find(':input'));
  new_element.find('input').each(function() {
      console.log(this);

      var attr = $(this).attr('id');
      if (typeof attr !== typeof undefined && attr !== false) {
        var id = attr.replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
        $(this).attr({'name': id, 'id': id}).val('').removeAttr('checked');
      }
  });
  new_element.find('select').each(function() {
      console.log(this);

      var attr = $(this).attr('id');
      if (typeof attr !== typeof undefined && attr !== false) {
        var id = attr.replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
        $(this).attr({'name': id, 'id': id}).val('').removeAttr('checked');
      }
  });
  new_element.find('label').each(function() {
    var attr = $(this).attr('for');
    if (typeof attr !== typeof undefined && attr !== false) {
      var new_for = attr.replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
      $(this).attr('for', new_for);
    }
  });

  // Replace for select fieds guids
  new_element.find('div[class=select-wrapper]').each(function() {
    var uuid = guid();
    console.log(uuid)
    $(this).find('[class*=select-dropdown]').each(function() {

      var attr = $(this).attr("data-activates");
      if (typeof attr !== typeof undefined && attr !== false) {
        $(this).attr('data-activates', 'select-options-' + uuid);
      }

      var attr = $(this).attr("id");
      if (typeof attr !== typeof undefined && attr !== false) {
        console.log("Changing data-activates attribute")
        console.log(this)
        $(this).attr('id', 'select-options-' + uuid);

      }
    });
  });

  // $('select').material_select();
  // $('input').material_input();
  $(selector).last().after(new_element);
}


function guid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}
//select-options-1947a5cd-0988-1104-9647-afd1d44a03c1

console.log($('input.select-dropdown:last'));
$('select[id=search_fields-1-field_type]').siblings('input').click(function(){
  console.log("Something")
})
