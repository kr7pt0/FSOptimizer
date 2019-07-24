angular.module('app')
.controller('ApplicationController', function ($window, $scope, $location) {

    $scope.triggerLineups = function(){

        $window.location.href = '#/lineup';

    }

    $scope.triggerPlayers = function(){

        $window.location.href = '#/';

    }
})