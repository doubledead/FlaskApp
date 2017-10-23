'use strict';

var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var browserSync = require('browser-sync');
var del = require('del');
var cache = require('gulp-cache');
var concat = require('gulp-concat');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var runSequence = require('run-sequence');
var templateCache = require('gulp-angular-templatecache');

var reload = browserSync.reload;

var AUTOPREFIXER_BROWSERS = [
  'ie >= 10',
  'ie_mob >= 10',
  'ff >= 30',
  'chrome >= 34',
  'safari >= 7',
  'opera >= 23',
  'ios >= 7',
  'android >= 4.4',
  'bb >= 10'
];

// Clear gulp cache
gulp.task('clear', function (done) {
  return cache.clearAll(done);
});

// Copy All Files At The Root Level (app)
gulp.task('copy', function () {
  return gulp.src([
    'app/*',
    '!app/*.html',
    '!app/bower_components{,/**}',
    '!app/vendor{,/**}'
  ], {
    dot: true
  }).pipe(gulp.dest('dist'))
    .pipe($.size({title: 'copy'}));
});

// Optimize Images
gulp.task('images', function () {
  return gulp.src('app/images/**/*')
    .pipe($.cache($.imagemin({
      progressive: true,
      interlaced: true
    })))
    .pipe(gulp.dest('dist/images'))
    .pipe($.size({title: 'images'}));
});

gulp.task('fonts', function () {
  return gulp.src(['app/fonts/**'])
    .pipe(gulp.dest('dist/fonts'))
    .pipe($.size({title: 'fonts'}));
});

// Compile and Automatically Prefix Stylesheets
gulp.task('styles', function () {
  // For best performance, don't add Sass partials to `gulp.src`
  return gulp.src([
    'app/styles/**/*.scss',
    'app/styles/**/*.css'
  ])
    .pipe($.newer('.tmp/styles'))
    .pipe($.sourcemaps.init())
    .pipe($.sass({
      precision: 10
    }).on('error', $.sass.logError))
    .pipe($.autoprefixer({browsers: AUTOPREFIXER_BROWSERS}))
    .pipe(gulp.dest('.tmp/styles'))
    // Concatenate And Minify Styles
    .pipe($.if('*.css', $.cssnano()))
    .pipe($.size({title: 'styles'}))
    .pipe($.sourcemaps.write('./'))
    .pipe(gulp.dest('dist/styles'))
});

// Compile and minify CSS vendor Stylesheets
gulp.task('csslibs', function () {
  // For best performance, don't add Sass partials to `gulp.src`
  return gulp.src([
    './app/bower_components/bootstrap/dist/css/bootstrap.min.css'
  ])
    .pipe($.newer('.tmp/styles'))
    .pipe($.sourcemaps.init())
    .pipe($.sass({
      precision: 10
    }).on('error', $.sass.logError))
    .pipe($.autoprefixer({browsers: AUTOPREFIXER_BROWSERS}))
    .pipe(gulp.dest('.tmp/styles'))
    .pipe($.concat('vendor.css'))
    // Concatenate And Minify Styles
    .pipe($.if('*.css', $.cssnano()))
    .pipe($.size({title: 'csslibs'}))
    .pipe($.sourcemaps.write('./'))
    .pipe(gulp.dest('dist/styles'))
});

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

// Concatenate and minify JavaScript.
gulp.task('scriptsHost', function () {

  return gulp.src([
    // Note: Since we are not using useref in the scripts build pipeline,
    //       you need to explicitly list your scripts here in the right order
    //       to be correctly concatenated
    './host/app/scripts/templates.js',
    './host/app/scripts/main.js',
    './host/app/scripts/events/events.js',
    './host/app/scripts/events/controllers/controllers.js',
    './host/app/scripts/events/directives/directives.js',
    './host/app/scripts/events/services/item-service.js',
    './host/app/scripts/events/services/services.js'
  ])
    .pipe($.newer('.tmp/js/host'))
    .pipe($.sourcemaps.init())
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest('.tmp/host/js'))
    .pipe($.concat('host.min.js'))
    .pipe($.uglify({preserveComments: 'some'}))
    // Output files
    .pipe($.size({title: 'scriptsHost'}))
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest('js/host'))
});

// Concatenate and minify JavaScript.
gulp.task('scriptsEvents', function () {

  return gulp.src([
    // Note: Since we are not using useref in the scripts build pipeline,
    //       you need to explicitly list your scripts here in the right order
    //       to be correctly concatenated
    './events/app/scripts/templates.js',
    './events/app/scripts/main.js',
    './events/app/scripts/events/events.js',
    './events/app/scripts/events/controllers/controllers.js',
    './events/app/scripts/events/directives/event.js',
    './events/app/scripts/events/directives/directives.js',
    './events/app/scripts/events/services/services.js'
  ])
    .pipe($.newer('.tmp/js/events'))
    .pipe($.sourcemaps.init())
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest('.tmp/events/js'))
    .pipe($.concat('events.min.js'))
    .pipe($.uglify({preserveComments: 'some'}))
    // Output files
    .pipe($.size({title: 'scriptsEvents'}))
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest('js/events'))
});

// Concatenate and minify JavaScript vendor libraries.
gulp.task('jslibs', function () {

  return gulp.src([
    './node_modules/jquery/dist/jquery.min.js',
    './node_modules/moment/min/moment.min.js',
    './node_modules/bootstrap/dist/js/bootstrap.min.js'
  ])
    .pipe($.newer('.tmp/js/libs'))
    .pipe($.sourcemaps.init())
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest('.tmp/js/libs'))
    .pipe($.concat('libraries.min.js'))
    .pipe($.uglify({preserveComments: 'some'}))
    // Output files
    .pipe($.size({title: 'jslibs'}))
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest('js/libs'))
});

// Concatenate and minify JavaScript vendor libraries.
gulp.task('jsDatetimePicker', function () {

  return gulp.src([
    './node_modules/angular-bootstrap-datetimepicker/src/js/datetimepicker.js',
    './node_modules/angular-bootstrap-datetimepicker/src/js/datetimepicker.templates.js',
    './node_modules/angular-date-time-input/src/dateTimeInput.js'
  ])
    .pipe($.newer('.tmp/js/vendor'))
    .pipe($.sourcemaps.init())
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest('.tmp/js/vendor'))
    .pipe($.concat('datetimepicker.min.js'))
    .pipe($.uglify({preserveComments: 'some'}))
    // Output files
    .pipe($.size({title: 'jsDatetimePicker'}))
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest('js/vendor'))
});

// Concatenate and minify AngularJS libraries.
gulp.task('angular-libs', function () {

  return gulp.src([
    './node_modules/angular/angular.min.js',
    './node_modules/angular-animate/angular-animate.min.js'
  ])
    .pipe($.newer('.tmp/js/libs'))
    .pipe($.sourcemaps.init())
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest('.tmp/js/libs'))
    .pipe($.concat('angularjs.min.js'))
    .pipe($.uglify({preserveComments: 'some'}))
    // Output files
    .pipe($.size({title: 'angular-libs'}))
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest('js/libs'))
});

gulp.task('templates', function () {
  return gulp.src('app/templates/**/*.html')
    .pipe(templateCache({standalone: true}))
    .pipe(gulp.dest('app/scripts'));
});

gulp.task('templatesHost', function () {
  return gulp.src('host/app/templates/**/*.html')
    .pipe(templateCache({standalone: true}))
    .pipe(gulp.dest('host/app/scripts'));
});

gulp.task('templatesEvents', function () {
  return gulp.src('events/app/templates/**/*.html')
    .pipe(templateCache({standalone: true}))
    .pipe(gulp.dest('events/app/scripts'));
});

gulp.task('templatesCreate', function () {
  return gulp.src('create/app/templates/**/*.html')
    .pipe(templateCache({standalone: true}))
    .pipe(gulp.dest('create/app/scripts'));
});

gulp.task('watch', ['templatesCreate', 'templatesEvents', 'templatesHost'], function () {
  gulp.watch(['create/app/templates/**/*.html'], ['templatesCreate']);
  gulp.watch(['events/app/templates/**/*.html'], ['templatesEvents']);
  gulp.watch(['host/app/templates/**/*.html'], ['templatesHost']);
});

// Scan Your HTML For Assets & Optimize Them
gulp.task('html', function () {

  return gulp.src('app/**/*.html')
    .pipe($.useref({
      searchPath: '{.tmp,app}',
      noAssets: true
    }))
    // Minify any HTML
    .pipe($.if('*.html', $.htmlmin({
      removeComments: true,
      collapseWhitespace: true,
      collapseBooleanAttributes: true,
      removeAttributeQuotes: true,
      removeRedundantAttributes: true,
      removeEmptyAttributes: true,
      removeScriptTypeAttributes: true,
      removeStyleLinkTypeAttributes: true,
      removeOptionalTags: true
    })))
    // Output Files
    .pipe($.if('*.html', $.size({title: 'html', showFiles: true})))
    .pipe(gulp.dest('dist'));
});

// Clean Output Directory
gulp.task('clean', del.bind(null, ['.tmp', 'dist/*', '!dist/.git'], {dot: true}));

// Remove unused build directories
gulp.task('remove', function() {
  del([
    'dist/templates'
  ]);
});

// Default task for Host JS module
gulp.task('host', [], function (cb) {
  runSequence(
    ['templatesHost'], cb
  );
});

gulp.task('create', [], function (cb) {
  runSequence(
    ['templatesCreate'], cb
  );
});

gulp.task('deployBuild', ['clean'], function (cb) {
  runSequence(
    ['scriptsHost', 'jslibs', 'angular-libs', 'jsDatetimePicker'], cb
  );
});
