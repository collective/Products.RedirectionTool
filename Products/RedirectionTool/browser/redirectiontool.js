jQuery(function($) {
    $('#alias-input-filter').typeWatch({
        wait: 150,
        callback: function(value) {
            $.ajax({
                url: '@@aliases-batch.json',
                data: {value: value},
                dataType: 'json',
                success: function(data) {
                    if (value.length >= 3) {
                        $('#redirectsTable tfoot').hide();  // hide pagination
                        $('#alias-input-filter-count').html(' (' + data.length + ')');
                    } else {
                        // no value - show full list including pagination
                        $('#redirectsTable tfoot').show();  // show pagination
                        $('#alias-input-filter-count').html('');
                    }
                    var tbody = $('#redirectsTable tbody'),
                        trow;
                    tbody.empty();
                    data.forEach(function(item, idx) {
                        trow = $('<tr class="' + (idx % 2 === 0 ? 'odd' : 'even') + '">' +
                          '<td><input type="checkbox" class="noborder" name="redirects:tuple" value="' + item.redirect + '" /></td>' +
                          '<td>' + item.path + '</td>' +
                          '<td>' + item['redirect-to'] + '</td>' +
                          '</tr>'
                        );
                        tbody.append(trow);
                    });
                }
            });
        },
        highlight: true,
        captureLength: 1
    });
});

