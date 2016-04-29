function addRowOld() {
$(document).ready(function() {
    var row = 1;
    var array = new Array();
    $('select').material_select();
    $('#customSearchOptions').hide();
    $('#customizeSearch').click(function() {
        $('#customSearchOptions').toggle();
    });
    $("#addButton").click(
        //Don't know how to simplify this, but this NEEDS TO BE SIMPLIFIED!!!!
        function() {
            var newRow = row++
                var deleteButtonID = "deleteButton_" + newRow;
            $("#newRow").append(' <div class="row animated fadeInUp" data-row="'+newRow+'" id="'+newRow+'"><div class="input-field col s2 offset-s2">Search Field Name:<br>{{ form.fieldname(size=120) }}<br></div><div class="input-field col s2">Description:<br>{{ form.description(size=120) }}<br></div><div class="input-field col s2">{{form.header}}</div><div class="input-field col s2">{{form.display}}</div><div class="col s2"><a class="waves-effect waves-teal btn-flat" id="' + deleteButtonID + '" onclick="deleteRow(this);"><i class="tiny material-icons black-text">delete</i></a></div>');
            $('select').material_select();
            //returning row ID (number)
        }); //end of add button click event functions
}); //end of document ready
}
// Logic for deleting row by row ID
function deleteRow_old(value) {
    var id = $(value).attr("id");
    rowid = id.split("_");
    $("#" + rowid[1]).remove();
}
