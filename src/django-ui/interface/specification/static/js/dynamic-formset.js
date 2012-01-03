   function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+)');
	var replacement = prefix + '-' + ndx;
	if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
	if (el.id) el.id = el.id.replace(id_regex, replacement);
	if (el.name) el.name = el.name.replace(id_regex, replacement);
   }   

    function addForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        var row = $('.dynamic-form:first').clone(true).get(0);
        $(row).removeAttr('id').insertAfter($('.dynamic-form:last')).children('.hidden').removeClass('hidden');
        $(row).children().not(':last').children().each(function() {
    	    updateElementIndex(this, prefix, formCount);
    	    $(this).val('');
        });
        $(row).find('.delete-row').click(function() {
    	    deleteForm(this, prefix);
        });
        $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
        return false;
    }

    function deleteForm(btn, prefix) {
        $(btn).parents('.dynamic-form').remove();
        var forms = $('.dynamic-form');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
    	    $(forms.get(i)).children().not(':last').children().each(function() {
    	        updateElementIndex(this, prefix, i);
    	    });
        }
        return false;
    }



    <script type="text/javascript">
    <!--
    $(function () {
        $('.add-row').click(function() {
    	    return addForm(this, 'form');
        });
        $('.delete-row').click(function() {
    	    return deleteForm(this, 'form');
        })
    })
    //-->
    </script>
    <table id="id_forms_table" border="0" cellpadding="0" cellspacing="5">
        <thead>
    	    <tr>
    	        <th scope="col">&nbsp;</th>
    	        <th scope="col">Property name</th>
    	        <th scope="col">&nbsp;</th>
    	        <th scope="col">&nbsp;</th>
    	    </tr>
        </thead>
        <tbody>
            {% for form in property_formset.forms %}
    	    <tr id="{{ form.prefix }}-row" class="dynamic-form">
    	        <td{% if forloop.first %} class="hidden"{% endif %}>{{ form.operand }}</td>
    	        <td>{{ form.property }}</td>
    	        <td>contains {{ form.value }}</td>
    	        <td{% if forloop.first %} class="hidden"{% endif %}>
    	            <a id="remove-{{ form.prefix }}-row" href="javascript:void(0)" class="delete-row"></a>
    	        </td>
            </tr>
    	    {% endfor %}
            <tr>
    	        <td colspan="4"><a href="javascript:void(0)" class="add-row">add property</a></td>
    	    </tr>
        </tbody>
    </table>
    {{ property_form.management_form }}
    <div>
        <input type="submit" value=" Find &raquo; " />
    </div>
