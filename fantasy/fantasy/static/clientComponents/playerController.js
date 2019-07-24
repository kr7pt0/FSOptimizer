angular.module('app')
.controller('PlayerController', function ($scope,
                                       $window,
                                       $rootScope,
                                       $http,
                                       PlayerService,
                                       LineupService) {


    $scope.generateLineup = function(){

        if($scope.projection === ""){
            window.alert("Select projection")
            return;
        }

        if($scope.site === ""){
            window.alert("Select site")
            return;
        } 

        if(angular.equals($scope.slate, {})){
            window.alert("Select slate")
            return;
        } 

        if($scope.data.length == 0){
            window.alert("Sorry, there is no input! Click <Load> button")
            return;
        } 

        $scope.isgenerating = true

        if (typeof $scope.lineupnumber === "undefined") {
            $scope.lineupnumber = 50
        }

        sessionStorage.setItem('table_data', JSON.stringify($scope.data))
        sessionStorage.setItem('temp_data', JSON.stringify($scope.temp_data))
        sessionStorage.setItem('lineup_data', JSON.stringify($scope.lineup_data))

        // console.log("Trigger generate lineup. number: " + $scope.lineupnumber)

        PlayerService.pushPlayers($scope.lineup_data, $scope.temp_data, $scope.lineupnumber, $scope.site, $scope.projection).then(function(result){
            $scope.isgenerating = false
            console.log("CUSTOM OPTIMIZER......")
            console.log(JSON.stringify(result.lineups))
            LineupService.setLineups(result.lineups)
            LineupService.setExport(result.export)
            $window.location.href = '#/lineup';
        })
    }

    $scope.uploadPlayers = function(){

        $window.location.href = '/';
    }

    $scope.setGlobalExposure = function(){

        $scope.initPlayers($scope.globalexposure)
    }

    //init
    $scope.isgenerating = false
    $scope.data = []
    $scope.lineup_data = []
    $scope.temp_data = []
    $scope.lineupnumber = 10
    $scope.globalexposure = 50
    $scope.site = ""
    $scope.slate_list = []
    $scope.slate = {}
    $scope.projection = ''

    $scope.lineupdata = []

    $scope.resetPlayers = function(){
        $scope.initPlayers(50, false)
    }

    $scope.columnNames = ["Lock","Remove","Name", "Salary", "Position", "TeamAbbrev", "Projection", "Custom", "Exposure"]

    // Charts
    $scope.table = PlayerTable()
        .on('edit', function(d) {
            
            $scope.data = JSON.parse(JSON.stringify(d.slice(1)))

            for (var i=0,len=$scope.temp_data.length; i<len; i++){
                var new_array = []
                new_array = d.slice(1)[i]
                new_array.push($scope.temp_data[i][9])
                $scope.temp_data[i] = new_array
                $scope.lineup_data[i][4] = d.slice(1)[i][6]
                $scope.lineup_data[i][5] = d.slice(1)[i][7]
                $scope.lineup_data[i][6] = d.slice(1)[i][8]
            }
        })

    $scope.updateTable = function updateTable(_data){
        d3.select('#magicdiv')
            .datum(_data)
            .call($scope.table);
    }

    $scope.initPlayers = function(exposure, isInit) {
        PlayerService.getPlayers(exposure, $scope.slate["id"]).then(function (devs) {
            if (isInit){
                $scope.lineupnumber = 1
                $scope.globalexposure = 50
                $scope.site = ""
                $scope.projection = ""
                // console.log("pull devs from db: " + devs)
                $scope.siteOptions = [
                    { name: 'DRAFTKINGS', value: 'DRAFTKINGS' },
                    { name: 'FANDUEL', value: 'FANDUEL' },
                ];
            }

            d3.select('#magicdiv').selectAll("*").remove()
            
            $scope.data = devs[0]
            $scope.lineup_data = devs[1]
            $scope.temp_data = devs[2]
            $scope.updateTable([$scope.data, $scope.columnNames])
        })
    }
    $scope.loadSlates = function() {
        PlayerService.getSlates($scope.site).then(function (devs) {
            $scope.slate_list = devs;
            $scope.slate = $scope.slate_list[0]
            $rootScope.slate_list = devs
            $rootScope.site = $scope.site
        })
    }

    $scope.loadPlayers = function() {
        if(angular.equals($scope.slate, {})){
            window.alert("Select slate")
            return;
        } 
        $rootScope.slate = $scope.slate
        $rootScope.globalexposure = $scope.globalexposure
        $scope.initPlayers($scope.globalexposure, false)
    }
    if(typeof $rootScope.slate !== 'undefined'){
        $scope.data = JSON.parse(sessionStorage.getItem('table_data'))
        $scope.temp_data = JSON.parse(sessionStorage.getItem('temp_data'))
        $scope.lineup_data = JSON.parse(sessionStorage.getItem('lineup_data'))
        $scope.slate_list = $rootScope.slate_list
        $scope.slate = $rootScope.slate
        $scope.site = $rootScope.site
        $scope.globalexposure = $rootScope.globalexposures

        d3.select('#magicdiv').selectAll("*").remove()
        $scope.updateTable([$scope.data, $scope.columnNames])
    }

})