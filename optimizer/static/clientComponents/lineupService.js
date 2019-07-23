angular.module('app')
.service('LineupService', function ($http) {
  var svc = this

  svc.lineups = []
  svc.export = []

  svc.setLineups = function (lineups) {
    svc.lineups = lineups
  }

  svc.setExport = function (data) {
      svc.export = data
  }

  svc.getLocalLineups = function () {
    return svc.lineups
  }

  svc.getLocalExport = function () {
      return svc.export
  }

})