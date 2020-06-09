var assert = require('assert')
var resolve = require('path').resolve
var exists = require('fs').exists

describe('win-7zip', function(){

  it('should get path of 7z.exe', function(done){
    var _7z_exe = resolve(__dirname, '7zip-lite/7z.exe')
    var _7z = require('./')['7z']

    assert.equal(_7z, _7z_exe)
    exists(_7z, function(flag){
      assert(flag)
      done()
    })
  })

})
