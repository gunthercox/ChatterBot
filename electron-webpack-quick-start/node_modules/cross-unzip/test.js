'use strict'
const unzip = require('./')

unzip('归档.zip', './abc', (err) => {
  console.error(err)
})
