/*
    Dynamically creates or deletes comment formset
    rows on stereotype management.
*/

// Receives the class of the formset rows and add a new row
function addNewFormsetRow(formsetRowClass) {
    var newFormsetRow = $(formsetRowClass).clone(true);
    var totalFormsetRows = $('.comment_select').length

    // Set new attributes for the select of the new row
    newFormsetRow.find('select').each(function() {
        var name = $(this).attr('name')
                    .replace('-' + (totalFormsetRows-1) + '-', '-' + (totalFormsetRows) + '-');
        
        var id = 'id_' + name;
        this.setAttribute("name", name);
        this.setAttribute("id", id);
    });

    // newFormsetRow.find('.comment_select').each(function() {
    //     $("option[value='" + selected + "']", $(this).attr('disabled', true));
    // });

    $('#id_' + prefix + '-TOTAL_FORMS').val(totalFormsetRows+1);
    
    $(selector).after(newElement);
}

$(document).on('click', '.add-formset-row', function(e) {
    e.preventDefault();
    addNewFormsetRow('.form-row:last');
    return false;
});