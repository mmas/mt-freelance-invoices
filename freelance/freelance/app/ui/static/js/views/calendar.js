views.Calendar = function(calendar) {

    var dates, selected_date;

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
            }
        }
    });

    dates = {};

    $.ajax({
        type: 'GET',
        url: '/api/days'
    })
    .done(function(data) {
        dates = data;
        renderSelectedDays();
    });

    calendar.$element.bind('widgets.calendar:change', function(e, $calendar, date) {
        if (date) selected_date = date;
    });

    calendar.$element.bind('widgets.calendar:render', function(e, date) {
        selected_date = date;
        renderSelectedDays();
    });

    this.selectDay = function() {
        var $cell;
        if (selected_date) {
            $cell = calendar.get(selected_date.isodate());
            if ($cell.attr('data-selected')) {  // TODO: get this info from data.
                deleteDay();
            }
            else {
                saveDay();
            }
        }
    };

    this.selectHalfDay = function() {
        if (selected_date) saveDay(true);
    };

    this.selectWorkweek = function() {
        // REDO
        // if (selected_date) {
        //     getWorkWeek().each(function() {
        //         this.removeAttribute('data-half');
        //         $(this).attr('data-selected', true);
        //     });
        // }
    };

    this.selectWeek = function() {
        // REDO
        // if (selected_date) {
        //     getWeek().each(function() {
        //         this.removeAttribute('data-half');
        //         $(this).attr('data-selected', true);
        //     });
        // }
    };

    function getWeek() {
        return calendar.get(selected_date.isodate()).parent().children();
    }

    function getWorkWeek() {
        return getWeek.slice(0, 5);
    }

    function saveDay(half) {
        half = half || false;
        $.ajax({
            url: '/api/day',
            type: 'POST',
            data: JSON.stringify({date: selected_date.isodate(), half: half})
        })
        .done(function(data) {
            var $cell;
            if (!data.saved) {
                $cell = calendar.get(data.date);
                if (data.half) {
                    $cell.attr('data-half', true);
                    $cell[0].removeAttribute('data-selected');
                }
                else {
                    $cell.attr('data-selected', true);
                    $cell[0].removeAttribute('data-half');
                }
            }
        })
    }

    function deleteDay() {
        $.ajax({
            url: '/api/day',
            type: 'DELETE',
            data: JSON.stringify({date: selected_date.isodate()})
        })
        .done(function(data) {
            var $cell;
            $cell = calendar.get(selected_date.isodate());
            $cell[0].removeAttribute('data-selected');
            $cell[0].removeAttribute('data-half');
        });
    }

    function renderSelectedDays() {
        var $cell, i, xi;
        for (i=0; xi=dates[i]; i++) {
            $cell = calendar.get(xi.date);
            console.log(xi);
            if ($cell) {
                if (xi.saved) $cell.attr('data-saved', true);
                else if (xi.half) $cell.attr('data-half', true);
                else $cell.attr('data-selected', true);
            }
        }
    }

};