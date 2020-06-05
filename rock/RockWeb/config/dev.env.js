"use strict";
const merge = require("webpack-merge");
const prodEnv = require("./dev.env");
module.exports = merge(prodEnv, {
  NODE_ENV: process.env.NODE_ENV,
  // BASE_API: process.env.BASE_API

  BASE_API: '"http://127.0.0.1:8000/"',
});
