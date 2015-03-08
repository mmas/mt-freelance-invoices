views.Calendar = function(calendar) {

    var view, model;

    view = this;
    model = {
        data: [],
        selected: []
    }
    model.diff = function() {
        // Filter out selected data based on 'date' key.
        var data, i, xi, j, xj;
        data = [];
        for (i=0; xi=model.selected[i]; i++) {
            for (j=0; xj=model.data[j]; j++) {
                if (xi.date != xj.date) {
                    data.push(xj);
                }
            }
        }
        model.data = data;
    };

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
            }
        },
        url: '/api/days'
    });

    $.ajax({
        type: 'GET',
    })
    .done(function(data) {
        model.data = data;
        render();
    });

    calendar.$element.bind('widgets.calendar:change', function(e, $calendar, date) {
        if (date) model.selected = [{date: utils.isodate(date)}];
    });

    calendar.$element.bind('widgets.calendar:render', function(e, date) {
        console.log('widget redered');
        model.selected = [{date: utils.isodate(date)}];
        render();
    });

    this.selectDay = function() {
        var $cell;
        if (model.selected.length) {
            $cell = calendar.cell(model.selected[0].date);
            if ($cell.attr('data-selected')) {  // TODO: get this info from data.
                delete_();
            }
            else {
                update();
            }
        }
    };

    this.selectHalfDay = function() {
        if (model.selected.length) {
            model.selected = [{date: model.selected[0].date, half: true}];
            update();
        }
    };

    this.selectWorkweek = function() {
        var selected = [];
        if (model.selected.length) {
            getWorkWeekCells(model.selected[0].date).each(function() {
                selected.push({date: utils.isodate(calendar.date(this))});
            });
            model.selected = selected;
            update();
        }
    };

    this.selectWeek = function() {
        var selected = [];
        if (model.selected.length) {
            getWeekCells(model.selected[0].date).each(function() {
                selected.push({date: utils.isodate(calendar.date(this))});
            });
            model.selected = selected;
            update();
        }
    };

    function getWeekCells(date) {
        return calendar.cell(date).parent().children();
    }

    function getWorkWeekCells(date) {
        return getWeekCells(date).slice(0, 5);
    }

    function update() {
        $.ajax({
            type: 'POST',
            data: JSON.stringify(model.selected)
        })
        .done(function(resp) {
            var i, xi, $cell;
            for (i=0; xi=resp[i]; i++) {
                if (!xi.invoice) {
                    $cell = calendar.cell(xi.date);
                    if (xi.half) {
                        $cell.attr('data-half', true);
                        $cell[0].removeAttribute('data-selected');
                    }
                    else {
                        $cell.attr('data-selected', true);
                        $cell[0].removeAttribute('data-half');
                    }
                }
            }
        })
    }

    function delete_() {
        $.ajax({
            type: 'DELETE',
            data: JSON.stringify(model.selected)
        })
        .done(function() {
            var i, xi, $cell;
            for (i=0; xi=model.selected[i]; i++) {
                $cell = calendar.cell(xi.date);
                if ($cell) {
                    $cell[0].removeAttribute('data-saved');
                    $cell[0].removeAttribute('data-half');
                    $cell[0].removeAttribute('data-selected');
                }
            }
            model.diff();
        });
    }

    function render() {
        var i, xi, $cell;
        for (i=0; xi=model.data[i]; i++) {
            $cell = calendar.cell(xi.date);
            if ($cell) {
                if (xi.invoice) $cell.attr('data-saved', true);
                else if (xi.half) $cell.attr('data-half', true);
                else $cell.attr('data-selected', true);
            }
        }
    }

};