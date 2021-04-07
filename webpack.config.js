'use strict';

const path = require('path');

const ManifestPlugin = require('webpack-manifest-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const LiveReloadPlugin = require('webpack-livereload-plugin');

const ENVIRONMENT = process.env.ENVIRONMENT;

// we don't want to use content hashed file names in development otherwise we'll end up
// with a million files when we're running webpack watch.
const staticNameFormat = ENVIRONMENT === 'development' ? '[name]' : '[name].[contenthash]'


module.exports = {
  mode: 'production',
  entry: [
    './frontend/js/main.js',
    './frontend/scss/main.scss',
  ],
  output: {
    filename: `static/js/${staticNameFormat}.js`,
    path: path.resolve(__dirname, 'app'),
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
              postcssOptions: {
                plugins: [
                  require('autoprefixer'),
                  require('tailwindcss'),
                ],
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
          return !file.path.match(/\/img\//);  // don't add image files to the manifest
        }
      }),
      new MiniCssExtractPlugin({
        filename: `static/css/${staticNameFormat}.css`,
        path: path.resolve(__dirname, '..', 'app'),
      }),
      new CopyPlugin(
        {'patterns': [
          {
            from: path.join(__dirname, 'frontend', 'img'),
            to: path.join(__dirname, 'app', 'static', 'img')
          },
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
