###bs-snippet-injector
Write & Remove the BrowserSync Snippet to a file

This is an alternative to using the BrowserSync proxy.

##Install 

```bash
$ npm install browser-sync bs-snippet-injector
```

###Example

```js
// requires version 1.3.3 of BrowserSync or higher.
var browserSync = require("browser-sync");

// register the plugin
browserSync.use(require("bs-snippet-injector"), {
    // path to the file containing the closing </body> tag
    file: "app/design/frontend/project/template/page/1column.phtml" 
});

// now run BrowserSync, wathching CSS files.
browserSync({
  files: "skin/frontend/project/assets/css/*.css"
});
```