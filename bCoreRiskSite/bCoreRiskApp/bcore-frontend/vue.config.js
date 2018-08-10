var BundleTracker = require('webpack-bundle-tracker')
var WriteFilePlugin = require('write-file-webpack-plugin')
var path = require('path')

module.exports = {
  configureWebpack: {
    // Merged into the final Webpack config
    plugins: [
      new BundleTracker({filename: './webpack-stats.json'}),
      new WriteFilePlugin()
    ],
    entry: './src/main.js',
    output: {
      filename: 'bundle.js'
    },
  },
  baseUrl: '/static'

}