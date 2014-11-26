/* jshint unused: false */

'use strict';

var gulp = require('gulp');
var requireDir = require('require-dir');
var dir = requireDir('./tasks');

var plugins = require('gulp-load-plugins')();

// js templates
gulp.task('templates', function(){
  gulp.src('cla_public/static-src/javascripts/templates/*.hbs')
    .pipe(plugins.handlebars())
    .pipe(plugins.defineModule('plain'))
    .pipe(plugins.declare({
      namespace: 'CLA.templates'
    }))
    .pipe(plugins.concat('templates.js'))
    .pipe(gulp.dest('cla_public/static-src/javascripts'));
});

gulp.task('build', [
    'minify-css',
    'templates',
    'minify-scripts',
    'images'
  ]
);

gulp.task('default', ['build']);
