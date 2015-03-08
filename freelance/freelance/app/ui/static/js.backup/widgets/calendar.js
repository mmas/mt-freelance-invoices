widgets.Calendar = function(element, context) {

    var widget, utils, $calendar;

    widget = this;
    utils = {
        mod: function(x, n) {
            // Fix modulo. Javascript hates Maths.
            // x: Number; n: Number.
            return ((x % n) + n) % n;
        },
        int: function(x) {
            // Bitwise. Faster than parseInt or Math.floor.
            // x: String
            return x | 0;
        },
        isodate: function(x) {
            // Format date as 'yyyy-mm-dd'.
            // x: Date.
            return x.toJSON().split('T')[0];
        }
    };
    $calendar = $(element);
    this.$element = $calendar;

    this.cell = function(date_str) {
        // Return td.day wich corresponds with the date passed (yyyy-mm-dd).
        var date, current_date, $cell;
        current_date = getCalendarDate();
        date = date_str.split('-');
        if (utils.int(date[0]) == current_date[0] && utils.int(date[1]) == current_date[1] + 1) {
            $cell = $calendar.find('td[data-month=' + current_date[1] + '][data-day=' + utils.int(date[2]) + ']');
            if ($cell.length) return $cell;
        }
    };

    this.date = function($cell) {
        // Return date (Date object) the $cell (td.day) or the currently selected if not $cell is passed.
        var date;
        if ($cell === undefined) {
            date = $calendar.attr('data-value');
            date = (date) ? new Date(date) : null;
            return date;
        }
        else {
            $cell = $($cell);
            return new Date(
                utils.int($calendar.attr('data-year')),
                utils.int($cell.attr('data-month')),
                utils.int($cell.attr('data-day')),
                12
            );
        }
    };

    this.refresh = function() {
        renderDays(widget.date() || new Date(), false);
    }

    render();
    $calendar.find('button.prev').bind('click', onClickCalendarPrev);
    $calendar.find('button.next').bind('click', onClickCalendarNext);
    $calendar.find('button.today').bind('click', onClickCalendarToday);
    $calendar.on('click', '.day', onClickCalendarDay);

    function onClickCalendarPrev(e) {
        var date;
        date = getCalendarDate();
        if (date[1] - 1 < 0) date[0]--;
        setCalendarDate(date[0], utils.mod((date[1] - 1), 12), 1);
        date = new Date(date[0], utils.mod((date[1] - 1), 12), 1, 12);
        renderDays(date);
    }

    function onClickCalendarNext(e) {
        var date;
        date = getCalendarDate();
        if (date[1] + 1 > 11) date[0]++;
        setCalendarDate(date[0], utils.mod((date[1] + 1), 12), 1);
        date = new Date(date[0], utils.mod((date[1] + 1), 12), 1, 12);
        renderDays(date);
    }

    function onClickCalendarToday(e) {
        var date;
        date = new Date();
        setCalendarDate(date.getFullYear(), date.getMonth(), date.getDate());
        renderDays(date);
    }

    function onClickCalendarDay(e) {
        var $day, date;
        date = getCalendarDate();
        $day = $(e.currentTarget);
        if ($day.hasClass('selected')) {
            $day.removeClass('selected');
            $calendar[0].removeAttribute('data-value');
            $calendar.trigger('widgets.calendar:change', [$calendar, null]);
        }
        else {
            date[2] = utils.int($day.attr('data-day'));
            setCalendarDate(date[0], date[1], date[2]);
            date = new Date(date[0], date[1], date[2], 12);
            $day.closest('tbody').find('.selected').removeClass('selected');
            $day.addClass('selected');
            $calendar.attr('data-value', utils.isodate(date));
            $calendar.trigger('widgets.calendar:change', [$calendar, date]);
        }
    }

    function getCalendarDate() {
        return [
            utils.int($calendar.attr('data-year')),
            utils.int($calendar.attr('data-month')),
            utils.int($calendar.attr('data-day'))
        ];
    }

    function setCalendarDate(year, month, day) {
        $calendar.attr('data-year', year);
        $calendar.attr('data-month', month);
        $calendar.attr('data-day', day || 1);
        $calendar.find('.month').text(context.months[utils.mod(month, 12)]);
        $calendar.find('.year').text(year);
    }

    function isToday(day, month, year) {
        var today;
        today = new Date();
        return today.getDate() == day && today.getMonth() == month && today.getFullYear() == year;
    }

    function isSelected(date_selected, day, month, year) {
        if (! date_selected) return false;
        return date_selected.getDate() == day && date_selected.getMonth() == month && date_selected.getFullYear() == year;
    }

    function render() {
        var $table, $header, $thead, $tbody, $row, date, i;
        date = widget.date() || new Date();
        setCalendarDate(date.getFullYear(), date.getMonth(), date.getDate());
        $header = $('<header />').appendTo($calendar);
        $header.append($('<span class="month" />').text(context.months[date.getMonth()]));
        $header.append($('<span class="year" />').text(date.getFullYear()));
        $header.append($('<button class="next" />').attr('title', context.next).text(context.next));
        $header.append($('<button class="prev" />').attr('title', context.prev).text(context.prev));
        $header.append($('<button class="today" />').attr('title', context.today).text(context.today));
        $table = $('<table />').appendTo($calendar);
        $thead = $('<thead />').appendTo($table);
        $row = $('<tr />').appendTo($thead);
        for (i in context.days) $row.append($('<th />').text(context.days[i]))
        $tbody = $('<tbody />').appendTo($table);
        renderDays(date);
    }

    function renderDays(date, trigger) {
        var $tbody, $row, $cell, $span, day, month, year, this_month, next_month, i, a_day, first_day_month,
            days_in_this_month, last_day_prev_month, week_day, remaining_days, date_selected;

        trigger = (trigger === undefined) ? true : trigger;  // Default=true.

        $tbody = $calendar.find('tbody');
        date_selected = $calendar.attr('data-value');
        if (date_selected) date_selected = new Date(date_selected);
        $tbody.empty();
        $row = $('<tr />').appendTo($tbody);
        day = date.getDate();
        month = date.getMonth();
        year = date.getFullYear();

        this_month = new Date(year, month, 1, 12);
        next_month = new Date(year, month + 1, 1, 12);

        // Find out when months start and end.
        a_day = 1000 * 60 * 60 * 24;
        first_day_month = this_month.getDay() - 1;  // Start week on Monday
        days_in_this_month = Math.round((next_month.getTime() - this_month.getTime()) / a_day);
        last_day_prev_month = new Date(this_month.getTime() - a_day).getDate();

        // Redefine if Sunday.
        first_day_month = utils.mod(first_day_month, 7);
        // Last days previous months and first week current month.
        for (i = first_day_month; i > 0; i--) {
            $cell = $('<td />').addClass('day prev').appendTo($row);
            $span = $('<span />').addClass('day-number').text(last_day_prev_month - i + 1).appendTo($cell);
        }

        // From second week of current month to end of month.
        week_day = Math.max(0, first_day_month); // Avoid to set a negative value if months starts by monday 1
        for (i = 1; i <= days_in_this_month; i++) {
            week_day = utils.mod(week_day, 7);
            if (week_day === 0) $row = $('<tr />').appendTo($tbody);
            $cell = $('<td />').addClass('day').attr('data-day', i).attr('data-month', month).appendTo($row);
            $span = $('<span />').addClass('day-number').text(i).appendTo($cell);
            if (isToday(i, month, year)) $cell.addClass('today');
            if (isSelected(date_selected, i, month, year)) $cell.addClass('selected');
            week_day++;
        }

        // First days of next month
        remaining_days = 7 - $row.find('span').length;
        for (i = 0; i < remaining_days; i++) {
            $cell = $('<td />').addClass('day next').appendTo($row);
            $span = $('<span />').addClass('day-number').text(i + 1).appendTo($cell);
        }

        // $calendar = $('#' + element.id);
        // this.$element = $calendar;
        if (trigger) $calendar.trigger('widgets.calendar:render', [date]);
    }
};