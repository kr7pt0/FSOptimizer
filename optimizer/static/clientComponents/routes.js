angular.module('app')
.config(function ($routeProvider) {
  $routeProvider
      
  .when('/',    { controller: 'PlayerController', templateUrl: 'templates/players.html' })
  .when('/lineup',    { controller: 'LineupController', templateUrl: 'templates/lineups.html' })

})
