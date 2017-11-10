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
    return del(['./project/static/scripts/js']);
});

gulp.task('default', ['del'], function () {
    gulp.start('transform');
    gulp.watch('./project/static/scripts/jsx/*.js', ['transform']);
});


// gulp.task('default', function () {
//     gulp.start('transform');
// });