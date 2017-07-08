; (function ($) {
    function get_forwards(element) {
        var forwardElem, forwardList, prefix, forwardedData, divSelector, form;
        divSelector = "div.dal-forward-conf#dal-forward-conf-for-" +
            element.attr("id");
        form = element.length > 0 ? $(element[0].form) : $();

        forwardElem =
            form.find(divSelector).find('script');
        if (forwardElem.length === 0) {
            return;
        }
        try {
            forwardList = JSON.parse(forwardElem.text());
        } catch (e) {
            return;
        }

        if (!Array.isArray(forwardList)) {
            return;
        }

        prefix = $(element).getFormPrefix();
        forwardedData = {};

        if(forwardList.some(e => e.src.includes('---'))){
            forwardedData['self'] = $(element).val()
        }

        $.each(forwardList, function (ix, f) {
            if (f["type"] === "const") {
                forwardedData[f["dst"]] = f["val"];
            } else if (f["type"] === "field") {
                var srcName = f["src"], 
                    dstName = f["dst"] || srcName;

                var wildcard = srcName.includes('---')
                var [sr1, sr2] = srcName.split('---')

                $field_selector = wildcard
                    ? '[name^=' + prefix + sr1 + ']' + '[name$=' + sr2 + ']'
                    : '[name=' + prefix + srcName + ']';


                $field = $($field_selector);
                if (!$field.length) {
                    
                    $field_selector = wildcard 
                        ? '[name^=' + sr1 + ']' + '[name$=' + sr2 + ']'
                        :'[name=' + srcName + ']';

                    $field = $($field_selector);
                }

                if ($field.length) {
                    if(wildcard){
                        forwardedData[dstName] = [...$field].map(e => $(e).val()).filter(e => e)
                    }else{
                        if ($field.attr('type') === 'checkbox')
                            forwardedData[dstName] = $field[0].checked;
                        else if ($field.attr('type') === 'radio')
                            forwardedData[dstName] = $($field_selector + ":checked").val();
                        else
                            forwardedData[dstName] = $field.val();
                    }
                }
            }
        });
        return JSON.stringify(forwardedData);
    }

    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]', function () {
        var element = $(this);

        // Templating helper
        function template(item) {
            if (element.attr('data-html') !== undefined) {
                var $result = $('<span>');
                $result.html(item.text);
                return $result;
            } else {
                return item.text;
            }
        }

        var ajax = null;
        if ($(this).attr('data-autocomplete-light-url')) {
            ajax = {
                url: $(this).attr('data-autocomplete-light-url'),
                dataType: 'json',
                delay: 250,

                data: function (params) {
                    var data = {
                        q: params.term, // search term
                        page: params.page,
                        create: element.attr('data-autocomplete-light-create') && !element.attr('data-tags'),
                        forward: get_forwards(element)
                    };

                    return data;
                },
                processResults: function (data, page) {
                    if (element.attr('data-tags')) {
                        $.each(data.results, function (index, value) {
                            value.id = value.text;
                        });
                    }

                    return data;
                },
                cache: true
            };
        }

        $(this).select2({
            tokenSeparators: element.attr('data-tags') ? [','] : null,
            debug: true,
            placeholder: '',
            minimumInputLength: 0,
            allowClear: !$(this).is('required'),
            templateResult: template,
            templateSelection: template,
            ajax: ajax,
        });
    });

    // Remove this block when this is merged upstream:
    // https://github.com/select2/select2/pull/4249
    $(document).on('DOMSubtreeModified', '[data-autocomplete-light-function=select2] option', function () {
        $(this).parents('select').next().find(
            '.select2-selection--single .select2-selection__rendered'
        ).text($(this).text());
    });
})(yl.jQuery);