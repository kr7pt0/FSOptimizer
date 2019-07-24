angular.module('app')
.service('PlayerService', function ($http) {
  var svc = this

  svc.getPlayers = function (exposure, slate){
    return $http.get('/api/players?slate=' + slate + "&exposure=" + exposure)
    .then(function (response) {
      return response.data
    })
  }

  svc.pushPlayers = function (lineup_data, players, lineups, site, projection) {
    return $http.post('/api/players', {
      lineup_data: lineup_data, players: players, lineups:lineups, site:site, projection:projection
    }).then(function (response) {
      return response.data
    })
  }

  svc.getSlates = function (site) {
    return $http.get('/api/slates?site=' + site + "&sport_type=PGA")
    .then(function (response) {
      return response.data
    })
  }

})