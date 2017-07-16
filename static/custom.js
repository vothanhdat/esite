; (function ($) {

    function get_forwardList(element) {
        var divSelector = "div.dal-forward-conf#dal-forward-conf-for-" + element.attr("id");
        var form = element.length > 0 ? $(element[0].form) : $();
        var forwardElem = form.find(divSelector).find('script');
        try {
            var forwardList = JSON.parse(forwardElem.text());
            if (forwardList instanceof Array)
                return forwardList;
            throw "";
        } catch (e) {
            return [];
        }


    }


    function get_forwards(element) {
        var forwardList = get_forwardList(element)

        if (!Array.isArray(forwardList)) {
            return;
        }

        var prefix = $(element).getFormPrefix();
        var forwardedData = {};

        $.each(forwardList, function (ix, f) {
            if (f.type === "const") {
                forwardedData[f.dst] = f.val;
            } else if (f.type === "field") {
                var srcName = f.src,
                    dstName = f.dst || srcName;

                if (srcName.includes('---'))
                    return;

                $field_selector = '[name=' + prefix + srcName + ']';


                $field = $($field_selector);
                if (!$field.length) {
                    $field_selector = '[name=' + srcName + ']';

                    $field = $($field_selector);
                }

                if ($field.length) {
                    if ($field.attr('type') === 'checkbox')
                        forwardedData[dstName] = $field[0].checked;
                    else if ($field.attr('type') === 'radio')
                        forwardedData[dstName] = $($field_selector + ":checked").val();
                    else
                        forwardedData[dstName] = $field.val();
                }
            }
        });
        return JSON.stringify(forwardedData);
    }

    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=customselect2]', function () {
        var element = $(this);
        var forwardList = get_forwardList(element)
        var prefix = $(element).getFormPrefix();

        if (forwardList.find(e => e.type == 'exclude')) {
            var exclude_field = forwardList.find(e => e.type == 'exclude')

            if (exclude_field && exclude_field.exclude) {
                var [pre, pos] = exclude_field.exclude.split('---')
                var $field_selector = '[name^=' + prefix + pre + ']' + '[name$=' + pos + ']'
                var $field_selector_bk = '[name^=' + pre + ']' + '[name$=' + pos + ']'
            }


        }
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
                    if ($field_selector) {
                        var $field = $($field_selector);
                        if (!$field.length)
                            $field = $($field_selector_bk);
                        var self = $(element).val()
                        var list_id = [...$field].map(e => $(e).val()).filter(e => e && e != self)
                        data.results = [...data.results]
                            .filter(e => e && e.id && list_id.indexOf(e.id) == -1)
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

        $(this).on('select2:selecting', function (e) {
            var data = e.params.args.data;

            if (data.create_id !== true)
                return;

            e.preventDefault();

            var select = $(this);

            $.ajax({
                url: $(this).attr('data-autocomplete-light-url'),
                type: 'POST',
                dataType: 'json',
                data: {
                    text: data.id,
                    forward: get_forwards($(this))
                },
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", document.csrftoken);
                },
                success: function(data, textStatus, jqXHR ) {
                    select.append(
                        $('<option>', {value: data.id, text: data.text, selected: true})
                    );
                    select.trigger('change');
                    select.select2('close');
                }
            });
        });


    });

    // Remove this block when this is merged upstream:
    // https://github.com/select2/select2/pull/4249
    $(document).on('DOMSubtreeModified', '[data-autocomplete-light-function=customselect2] option', function () {
        $(this).parents('select').next().find(
            '.select2-selection--single .select2-selection__rendered'
        ).text($(this).text());
    });

})(yl.jQuery);