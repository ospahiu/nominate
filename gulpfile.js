// requirements

var gulp = require('gulp');
var gulpBrowser = require("gulp-browser");
var reactify = require('reactify');
var del = require('del');
var size = require('gulp-size');


// tasks

gulp.task('transform', function () {
    var stream = gulp.src('./nominate/static/scripts/jsx/*.js')
        .pipe(gulpBrowser.browserify({transform: ['reactify']}))
        .pipe(gulp.dest('./nominate/static/scripts/js/'))
        .pipe(size());
    return stream;
});

gulp.task('del', function () {
    // add task
});

gulp.task('default', function () {
    gulp.start('transform');
});