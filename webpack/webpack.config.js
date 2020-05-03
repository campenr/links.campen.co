'use strict';

const path = require('path');
const glob = require('glob');

const ManifestPlugin = require('webpack-manifest-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const PurgecssPlugin = require('purgecss-webpack-plugin');
const LiveReloadPlugin = require('webpack-livereload-plugin');

const ENVIRONMENT = process.env.ENVIRONMENT;

// we don't want to use content hashed file names in development otherwise we'll end up
// with a million files when we're running webpack watch.
const staticNameFormat = ENVIRONMENT === 'development' ? '[name]' : '[name].[contenthash]'

module.exports = {
  mode: 'production',
  entry: [
    './frontend/js/index.js',
    './frontend/scss/main.scss',
  ],
  output: {
    filename: `static/js/${staticNameFormat}.js`,
    path: path.resolve(__dirname, '..', 'app'),
  },
  module: {
    rules: [
      {
        test: /\.(scss|css)$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
          },
          {
            loader: 'postcss-loader',
            options: {
              config: {
                path: './webpack',
              },
            },
          },
          {
            loader: 'sass-loader',
            options: {
              sassOptions: {
                outputStyle: 'compressed',
              }
            },
          },
        ],
      },
      {
        test: /.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
        use: [{
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'static/fonts/',
              publicPath: '../fonts/',
            }
        }]
    },
    ],
  },
  plugins: [
      new ManifestPlugin({
        fileName: 'static/webpack-manifest.json',
        map: (file) => {
          file.path = file.path.replace(/static\//, '');
          return file;
        },
        filter: (file) => {
          let include = true;
          if (file.path.match(/\/img\//)) {include = false}
          if (file.path.match(/\/fonts\//)) {include = false}
          return include
        }
      }),
      new MiniCssExtractPlugin({
        filename: `static/css/${staticNameFormat}.css`,
        path: path.resolve(__dirname, '..', 'app'),
      }),
      new CopyPlugin([
        {
          from: path.join(__dirname, '..', 'frontend', 'img'),
          to: path.join(__dirname, '..', 'app', 'static', 'img')
        },
      ]),
      new PurgecssPlugin({
        paths: glob.sync(`${path.join(__dirname, '..', 'app')}/**/*`,  { nodir: true }),
        whitelist: [
          'col-sm-12', 'col-md-5', 'col-md-7',
          'dataTables_wrapper', 'dt-bootstrap4', 'no-footer',
          'sorting', 'sorting_asc', 'sorting_desc', 'sorting_disabled',
          'table', 'table-striped', 'table-hover', 'dataTable',
          'link-table-body', 'odd', 'even', 'table', 'td', 'th', 'thead',
          'dataTables_paginate', 'paging_simple_numbers',
          'page-link', 'paginate_button', 'page-item', 'next', 'previous', 'disabled', 'active',
          'btn', 'copy-button',
          'fal', 'fa-copy', 'fa-trash',
        ]
      }),
      new LiveReloadPlugin({
        // because we're not using hashed file names when running webpack watch we need to check hashes here.
        useSourceHash: true,
      }),
  ],
  optimization: {
    splitChunks: {
      chunks: 'all',
    },
  },
  watchOptions: {
    ignored: /node_modules/,
  },
};
