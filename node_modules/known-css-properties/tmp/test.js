const data = require('./data');
const uniq = require('lodash.uniq');

console.log(
    uniq(
        data.map(entry => entry.status)
    )
)
    
