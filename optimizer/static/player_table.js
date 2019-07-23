var PlayerTable = function module() {
    var dispatch = d3.dispatch("edit");

    var lockTrueHtml = '<i style="color:limegreen" class="fa fa-lock "></i>'
    var lockFalseHtml = '<i style="color:indianred" class="fa fa-unlock "></i>'
    var removeTrueHtml = '<i style="color:indianred" class="fa fa-times "></i>'
    var removeFalseHtml = '<i style="color:limegreen" class="fa fa-check "></i>'

    var dataChange = function () {
        var newData = [];
        d3.select('.table').selectAll('tr').selectAll('td.cell')
            .each(function(d, i, pI){
                // console.log("rebind index: " + i + " second: " +pI + " d:" + d)
                if (i >1) {
                    var text = d3.select(this).text();
                    if (typeof newData[pI] == 'undefined') newData[pI] = [];
                    newData[pI].push(text)
                }
                if (i == 0){
                    var html = d3.select(this).html();
                    var value = 0
                    if (typeof newData[pI] == 'undefined') newData[pI] = [];
                    if (html == lockTrueHtml){
                        value = 1
                    }
                    newData[pI].push(value)
                }
                if (i == 1){
                    var html = d3.select(this).html();
                    var value = 0
                    if (typeof newData[pI] == 'undefined') newData[pI] = [];
                    if (html == removeTrueHtml){
                        value = 1
                    }
                    newData[pI].push(value)
                }
            });
        dispatch.edit(newData);

    }

    function exports(_selection) {
        _selection.each(function (_dataset) {

            //________________________________________________
            // Data
            //________________________________________________
            var data = _dataset[0];
            var columnNames = _dataset[1];

            //________________________________________________
            // Table
            //________________________________________________
            var table = d3.select(this).selectAll("table").data([0]);
            table.enter().append('table')
                .attr("class", "table table-striped")
                .append("thead")
                .append('tr')
                .selectAll('th')
                .data(columnNames)
                .enter().append('th')
                .text(function(d, i){return d;});

            var rows = table.append("tbody").selectAll('tr')
                .data(data);
            rows.enter().append('tr')

            var cells = rows.selectAll('td.cell')
                .data(function(d, i){return d;})
            cells.enter().append('td')
                .attr({class: 'cell', contenteditable: true});
            cells.text(function(d, i){return d;})
                .on("keyup", function(d, i){
                   dataChange()
                });

            // custom lock col
            cells.filter(function(d, i){ return i ==  0; })
                .attr({class: 'cell', contenteditable: false})
                .html(function(d,i) {
                    if (d == 0) {
                        return  lockFalseHtml

                    } else {
                        return lockTrueHtml
                    }
                })
                .on("click", function(d,i){
                    var currentHtml = d3.select(this).html()
                    if (currentHtml == lockTrueHtml) {
                        console.log("click 0 " + d3.select(this).html())
                        d3.select(this).html(lockFalseHtml)

                    } else {
                        d3.select(this).html(lockTrueHtml)
                    }
                    console.log("trigger click on lock")
                    dataChange();
                })

            // custom remove col
            cells.filter(function(d, i){ return i ==  1; })
                .attr({class: 'cell', contenteditable: false})
                .html(function(d,i) {
                    if (d == 0) {
                        return  removeFalseHtml

                    } else {
                        return removeTrueHtml
                    }
                })
                .on("click", function(d,i){
                    var currentHtml = d3.select(this).html()
                    if (currentHtml == removeTrueHtml) {
                        console.log("click 0 " + d3.select(this).html())
                        d3.select(this).html(removeFalseHtml)

                    } else {
                        d3.select(this).html(removeTrueHtml)
                    }
                    dataChange();
                })
        });
    }

    d3.rebind(exports, dispatch, "on");

    return exports;
};