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

// Lint JavaScript
gulp.task('lint', function () {
  return gulp.src([
    'app/scripts/**/*.js',
    '!node_modules/**',
    '!bower_components/**',
    '!app/scripts/templates.js'
  ])
    .pipe($.eslint())
    .pipe($.eslint.format())
    .pipe($.if(!browserSync.active, $.eslint.failAfterError()))
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

// Concatenate and minify JavaScript vendor libraries.
gulp.task('jslibs', function () {

  return gulp.src([
    // Note: Since we are not using useref in the scripts build pipeline,
    //       you need to explicitly list your scripts here in the right order
    //       to be correctly concatenated
    './app/bower_components/jquery/dist/jquery.min.js',
    './app/bower_components/moment/min/moment.min.js',
    './app/bower_components/bootstrap/dist/js/bootstrap.min.js',
    './app/bower_components/angular/angular.min.js',
    './app/bower_components/angular-route/angular-route.min.js',
    './app/bower_components/angular-animate/angular-animate.min.js',
    './app/vendor/angular-bootstrap-datetimepicker/js/datetimepicker.js',
    './app/vendor/angular-bootstrap-datetimepicker/js/datetimepicker.templates.js',
    './app/vendor/angular-date-time-input/dateTimeInput.js'
  ])
    .pipe($.newer('.tmp/bower_components'))
    .pipe($.sourcemaps.init())
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest('.tmp/bower_components'))
    .pipe($.concat('libraries.min.js'))
    .pipe($.uglify({preserveComments: 'some'}))
    // Output files
    .pipe($.size({title: 'jslibs'}))
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest('dist/scripts'))
});

gulp.task('templates', function () {
  return gulp.src('app/templates/**/*.html')
    .pipe(templateCache({standalone: true}))
    .pipe(gulp.dest('app/scripts'));
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

// Watch Files For Changes & Reload
gulp.task('serve', ['templates', 'scripts', 'jslibs', 'styles'], function () {
  browserSync.init({
    notify: false,
    // Customize the BrowserSync console logging prefix
    logPrefix: 'WSK',
    // Run as an https by uncommenting 'https: true'
    // Note: this uses an unsigned certificate which on first access
    // will present a certificate warning in the browser.
    // https: true,
    server: ['.tmp/', 'app'],
    port: 3000
  });
  gulp.watch(['app/index.html'], reload);
  gulp.watch(['app/templates/**/*.html'], ['templates', reload]);
  // gulp.watch(['app/scripts/**/*.js'], ['lint', 'scripts', reload]);
  gulp.watch(['app/scripts/**/*.js'], ['scripts', reload]);
  gulp.watch(['app/styles/**/*.{scss,css}'], ['styles', reload]);
  gulp.watch(['app/images/**/*'], reload);
});

// Build and serve the output from the dist build
gulp.task('serve:dist', ['default'], function () {
  browserSync({
    notify: false,
    logPrefix: 'WSK',
    // Run as an https by uncommenting 'https: true'
    // Note: this uses an unsigned certificate which on first access
    //       will present a certificate warning in the browser.
    // https: true,
    server: 'dist',
    port: 3001
  });
});

// Build Production Files, the Default Task
gulp.task('default', ['clean'], function (cb) {
  runSequence(
    'styles',
    // ['lint', 'html', 'templates', 'scripts', 'jslibs', 'csslibs', 'images', 'fonts', 'copy'],
    ['html', 'templates', 'scripts', 'jslibs', 'csslibs', 'images', 'fonts', 'copy'],
    'remove',
    cb
  );
});
