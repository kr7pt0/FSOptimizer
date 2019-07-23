angular.module('app')
.controller('LineupController', function ($scope,
                                       $window,
                                       $rootScope,
                                       $http,
                                       LineupService) {


    $scope.downloadLineup = function(){
        console.log("Trigger download.")

        var data = LineupService.getLocalExport()

        function exportToCsv(filename, rows) {
            var processRow = function (row) {
                var finalVal = '';
                for (var j = 0; j < row.length; j++) {
                    var innerValue = row[j] === null ? '' : row[j].toString();
                    if (row[j] instanceof Date) {
                        innerValue = row[j].toLocaleString();
                    };
                    var result = innerValue.replace(/"/g, '""');
                    if (result.search(/("|,|\n)/g) >= 0)
                        result = '"' + result + '"';
                    if (j > 0)
                        finalVal += ',';
                    finalVal += result;
                }
                return finalVal + '\n';
            };


            var csvFile = '';
            for (var i = 0; i < rows.length; i++) {

                csvFile += processRow(rows[i]);
            }

            var blob = new Blob([csvFile], { type: 'text/csv;charset=utf-8;' });
            if (navigator.msSaveBlob) { // IE 10+
                navigator.msSaveBlob(blob, filename);
            } else {
                var link = document.createElement("a");
                if (link.download !== undefined) { // feature detection
                    // Browsers that support HTML5 download attribute
                    var url = URL.createObjectURL(blob);
                    link.setAttribute("href", url);
                    link.setAttribute("download", filename);
                    link.style.visibility = 'hidden';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }
            }
        }

        exportToCsv("lineups.csv", data)
    }

    $scope.data = []
    $scope.columnNames = ["Position","Name","Team","Projection","Salary"]

    $scope.table = Table()
        .on('edit', function(d) {
            //console.log(JSON.stringify(d.slice(1)))
            $scope.data = d.slice(1)
        })

    $scope.updateTable = function updateTable(_data){
        d3.select('#lineupdiv')
            .datum(_data)
            .call($scope.table);
    }

    // fetch devs and log to console
    console.log("LOCAL LINEUPS...")
    console.log("LOCAL LINEUPS..." + JSON.stringify(LineupService.getLocalLineups()))

    d3.select('#magicdiv').selectAll("*").remove()

    //$scope.updateTable([$scope.data, $scope.columnNames])
    $scope.updateTable([LineupService.getLocalLineups(), $scope.columnNames])

    $scope.goBack = function(){
        history.back();
    }

})