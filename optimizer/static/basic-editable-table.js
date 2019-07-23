var Table = function module() {
    var dispatch = d3.dispatch("edit");

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
                    var newData = [];
                    console.log("rebind data")
                    d3.select('.table').selectAll('tr').selectAll('td.cell')
                        .each(function(d, i, pI){

                            var text = d3.select(this).text();
                            if (typeof newData[pI] == 'undefined') newData[pI] = [];
                            newData[pI].push(text)
                        });
                    dispatch.edit(newData);
                });
        });
    }

    d3.rebind(exports, dispatch, "on");

    return exports;
};