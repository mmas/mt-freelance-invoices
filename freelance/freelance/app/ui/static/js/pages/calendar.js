pages.Calendar = function(calendar) {

    var dates, i, selected_date;

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
            if ($cell.attr('data-selected') == 1) {
                $cell.attr('data-selected', 0);
                saveDay(0);
            }
            else {
                $cell.attr('data-selected', 1);
                saveDay(1);
            }
        }
    }

    this.selectHalfDay = function() {
        if (selected_date) {
            calendar.get(selected_date.isodate()).attr('data-selected', 2);
            saveDay(2);
        }
    }

    this.selectWorkweek = function() {
        if (selected_date) {
            calendar.get(selected_date.isodate()).parent().children().slice(0, 5).attr('data-selected', 1);
        }
    }

    this.selectWeek = function() {
        if (selected_date) {
            calendar.get(selected_date.isodate()).parent().children().attr('data-selected', 1);
        }
    }

    this.createInvoice = function() {

    }

    function saveDay(status) {
        $.ajax({
            url: '/api/day',
            type: 'POST',
            data: JSON.stringify({date: selected_date.isodate(), status: status})
        });
    }

    function renderSelectedDays() {
        var $cell;
        for (i=0; i<dates.length; i++) {
            $cell = calendar.get(dates[i].date)
            if ($cell) $cell.attr('data-selected', dates[i].status);
        }
    }

};