// Requires
const gulp = require('gulp'),
      sass = require('gulp-sass'),
      normalize = require('node-normalize-scss'),
      autoprefixer = require('gulp-autoprefixer');


/*
* Compile sass
*/
gulp.task('sass', () =>
  gulp.src('./scss/*.scss')
    .pipe(sass({
      includePaths: normalize.includePaths,  // adds normalize.css
      outputStyle: 'compressed'
    }).on('error', sass.logError))
    .pipe(autoprefixer({
      browsers: ['last 2 versions']
    }))
    .pipe(gulp.dest('./css'))
);


gulp.task('default', () => {
  gulp.watch('./scss/*.scss', ['sass']);
});
