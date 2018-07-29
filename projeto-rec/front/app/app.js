angular.module('recommendation',[]);

angular.module('recommendation')
.controller('MainCtrl', function ($scope, $http) {
    $scope.watchedMovies = [];
    $scope.result = [];
    var fullMovieList = [];
    $http.get("http://localhost:9090/api/movies").then(function (resp) {
        fullMovieList = resp.data;
        $scope.movies = fullMovieList.slice(0, 50);
        console.log(fullMovieList);
    });

    $scope.getRecommendations = function () {
        $http.post("http://localhost:9090/api/recommendation", {movie_ids: $scope.watchedMovies}, { headers: {'Content-Type': 'application/json; charset=UTF-8' }}).then(function (value) {
            $scope.result = value.data;
            for (var movie of $scope.result) {
                movie.name = getMovieName(movie.item_id);
                console.log(movie);
            }
            $scope.showResults = true;
        });
    };
    
    $scope.addMovie = function (movieId) {
        $scope.watchedMovies.push(movieId);
    };

    $scope.showAll = function () {
        $scope.movies = fullMovieList;
    };

    function getMovieName(id) {
        for (var movie of fullMovieList) {
            if (id === movie.id) {
                return movie.name
            }
        }
    }
    $scope.$watch('search', function (newVal) {
        if(newVal)
            $scope.movies = fullMovieList;
        else if (!newVal || newVal === '') {
            $scope.movies = fullMovieList.slice(0,50)
        }
    });
});
