var bs = require("browser-sync");

bs.use(require("./index"), {file: "index.html"});

bs();