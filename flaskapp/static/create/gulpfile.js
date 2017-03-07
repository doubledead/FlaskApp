'use strict';

var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var del = require('del');
var cache = require('gulp-cache');
var concat = require('gulp-concat');
var sourcemaps = require('gulp-sourcemaps');
var runSequence = require('run-sequence');
var templateCache = require('gulp-angular-templatecache');

// Concatenate and minify JavaScript.
gulp.task('scripts', function () {

  return gulp.src([
    // Note: Since we are not using useref in the scripts build pipeline,
    //       you need to explicitly list your scripts here in the right order
    //       to be correctly concatenated
    './app/scripts/templates.js',
    './app/scripts/main.js',
    './app/scripts/create/create.js',
    './app/scripts/create/controllers/controllers.js',
    './app/scripts/create/directives/directives.js',
    './app/scripts/create/services/create_service.js'
  ])
    .pipe($.newer('.tmp/scripts'))
    .pipe($.sourcemaps.init())
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest('.tmp/scripts'))
    .pipe($.concat('main.min.js'))
    .pipe($.uglify({preserveComments: 'some'}))
    // Output files
    .pipe($.size({title: 'scripts'}))
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest('dist/scripts'))
});

gulp.task('templates', function () {
  return gulp.src('app/templates/**/*.html')
    .pipe(templateCache({standalone: true}))
    .pipe(gulp.dest('app/scripts'));
});

// Default task that will run by type 'gulp'
gulp.task('default',['templates']);
