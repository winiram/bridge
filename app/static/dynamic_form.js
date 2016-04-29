$(document).ready(function () {
    $('select').material_select();

    $('#customSearchOptions').hide();
    $('#customizeSearch').click(function () {
        $('#customSearchOptions').toggle();
    });  
    var selector = 'div[class*=searchField]';
    var element = $('div[class*=searchField]').last().clone(true);
    
    $("a[class*=addButton]").click(function () {
        clone_field_list(element, selector);
    });
});

function clone_field_list(element1, selector1) {
    var new_element = element1.clone(true);
    var elem_id = $('div[class*=searchField]').last().find('input')[0].id;
    var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
new_element.find('input').each(function () {

        var attr = $(this).attr('id');
        if (typeof attr !== typeof undefined && attr !== false) {
            var id = attr.replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
            $(this).attr({
                'name': id,
                'id': id
            }).val('').removeAttr('checked');
        }
    });

    new_element.find('select').each(function () {

        var attr = $(this).attr('id');
        if (typeof attr !== typeof undefined && attr !== false) {
            var id = attr.replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
            $(this).attr({
                'name': id,
                'id': id
            }).val('').removeAttr('checked');
        }
    });

    new_element.find('a').each(function () {
        var attr = $(this).attr('id');
    });

    new_element.find('label').each(function () {
        var attr = $(this).attr('for');
        if (typeof attr !== typeof undefined && attr !== false) {
            var new_for = attr.replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
            $(this).attr('for', new_for);
        }
    });

    // Replace for select fieds guids
    new_element.find('div[class=select-wrapper]').each(function () {
        var uuid = guid();
        $(this).find('[class*=select-dropdown]').each(function () {
            var attr = $(this).attr("data-activates");
            if (typeof attr !== typeof undefined && attr !== false) {
                $(this).attr('data-activates', 'select-options-' + uuid);
            }
            var attr = $(this).attr("id");
            if (typeof attr !== typeof undefined && attr !== false) {
                $(this).attr('id', 'select-options-' + uuid);
            }
        });
    });
    new_element.find('a').parent().each(function () {
        $(this).children('a').remove();
        $(this).prepend("<a class='deleteButton waves-effect waves-teal btn-flat'> <i class='material-icons'>delete</i></a>");
    });
    
    $(selector1).last().after(new_element);
    $('select').material_select();
    $(".deleteButton").click(function () {
        $(this).parents('div[class*=searchField]').remove();
    });
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