# Sass Lint [![npm version](https://badge.fury.io/js/sass-lint.svg)](http://badge.fury.io/js/sass-lint) [![Build Status](https://travis-ci.org/sasstools/sass-lint.svg?branch=develop)](https://travis-ci.org/sasstools/sass-lint) [![Coverage Status](https://coveralls.io/repos/sasstools/sass-lint/badge.svg?branch=develop&service=github)](https://coveralls.io/github/sasstools/sass-lint?branch=develop) [![Dependency Status](https://david-dm.org/sasstools/sass-lint.svg)](https://david-dm.org/sasstools/sass-lint#info=dependencies&view=list) [![Dev Dependency Status](https://david-dm.org/sasstools/sass-lint/dev-status.svg)](https://david-dm.org/sasstools/sass-lint#info=devDependencies&view=list)

A Node-only Sass linter for both `sass` and `scss` syntax!

---

## Install
You can get `sass-lint` from [NPM](https://www.npmjs.com/package/sass-lint):

Install globally
```
npm install -g sass-lint
```

To save to a project as a dev dependency
```
npm install sass-lint --save-dev
```

---

## Configuring

Sass-lint can be configured from a `.sass-lint.yml` or `.sasslintrc` file in your project. The `.sasslintrc` file can be in either JSON format or YAML. Both formats are interchangeable easily using tools such as [json2yaml](https://www.json2yaml.com/). If you don't either file in the root of your project or you would like all your projects to follow a standard config file then you can specify the path to one in your project's `package.json` file with the `sasslintConfig` option.

For example:
```javascript
{
  "name": "my-project",
  "version": "1.0.0",
  "sasslintConfig": "PATH/TO/YOUR/CONFIG/FILE"
}
```

Use the [Sample Config (YAML)](https://github.com/sasstools/sass-lint/tree/master/docs/sass-lint.yml) or [Sample Config (JSON)](https://github.com/sasstools/sass-lint/tree/master/docs/sasslintrc) as a guide to create your own config file. The default configuration can be found [here](https://github.com/sasstools/sass-lint/blob/master/lib/config/sass-lint.yml).

### [Configuration Documentation](https://github.com/sasstools/sass-lint/tree/master/docs/options)

*Migrating from SCSS-Lint*: If you already have a config for SCSS-Lint, you can instantly convert it to the equivalent Sass Lint config at [sasstools.github.io/make-sass-lint-config](http://sasstools.github.io/make-sass-lint-config/).

### Options

The following are options that you can use to config the Sass Linter.

* [cache-config](https://github.com/sasstools/sass-lint/tree/master/docs/options/cache-config.md) - Allows you to cache your config for a small speed boost when not changing the contents of your config file
* [config-file](https://github.com/sasstools/sass-lint/tree/master/docs/options/config-file.md) - Specify another config file to load
* [formatter](https://github.com/sasstools/sass-lint/tree/master/docs/options/formatter.md) - Choose the format for any warnings/errors to be displayed
* [merge-default-rules](https://github.com/sasstools/sass-lint/tree/master/docs/options/merge-default-rules.md) - Allows you to merge your rules with the default config file included with sass-lint
* [output-file](https://github.com/sasstools/sass-lint/tree/master/docs/options/output-file.md) - Choose to write the linters output to a file

#### Files

The `files` option contains two properties, `include` and `ignore`. Both can be set to either a [glob](https://github.com/isaacs/node-glob) or an array of glob strings/file paths depending on your projects' needs and setup.

For example below we are providing a singular glob string to our include property and an array of patterns to our ignore property:
```yml
files:
  include: 'sass/**/*.s+(a|c)ss'
  ignore:
    - 'sass/vendor/**/*.scss'
    - 'sass/tests/**/*.scss'
```

As mentioned you can also provide an array to the include property like so
```yml
files:
  include:
    - 'sass/blocks/*.s+(a|c)ss'
    - 'sass/elements/*.s+(a|c)ss'
  ignore:
    - 'sass/vendor/**/*.scss'
    - 'sass/tests/**/*.scss'
```

#### Rules

For all [rules](https://github.com/sasstools/sass-lint/tree/master/docs/rules), setting their severity to `0` turns it off, setting to `1` sets it as a warning (something that should not be committed in), and setting to `2` sets it to an error (something that should not be written). If a rule is set to just a severity, it will use the default configuration (where available).

If you want to configure options, set the rule to an array, where the first item in the array is the severity, and the second item in the array is an object including the options you would like to set.

Here is an example configuration of a rule, where we are specifying that breaking the [indentation rule](https://github.com/sasstools/sass-lint/blob/master/docs/rules/indentation.md) should be treated as an error (its severity set to two), and setting the `size` option of the rule to 2 spaces:  

```yml
rules:
  indentation:
    - 2
    -
      size: 2
```

### [Rules Documentation](https://github.com/sasstools/sass-lint/tree/master/docs/rules)

---

## Disabling Linters via Source

Special comments can be used to disable and enable certain rules throughout your source files in a variety of scenarios. These can be useful when dealing with legacy code or with certain necessary code smells. You can read the documentation for this feature [here](https://github.com/sasstools/sass-lint/tree/master/docs/toggle-rules-in-src.md).

Below are examples of how to use this feature:


### Disable a rule for the entire file

```scss
// sass-lint:disable border-zero
p {
  border: none; // No lint reported
}
```

### Disable more than 1 rule

```scss
// sass-lint:disable border-zero, quotes
p {
  border: none; // No lint reported
  content: "hello"; // No lint reported
}
```

### Disable a rule for a single line

```scss
p {
  border: none; // sass-lint:disable-line border-zero
}
```

### Disable all lints within a block (and all contained blocks)

```scss
p {
  // sass-lint:disable-block border-zero
  border: none; // No result reported
}

a {
  border: none; // Failing result reported
}
```

### Disable and enable again

```scss
// sass-lint:disable border-zero
p {
  border: none; // No result reported
}
// sass-lint:enable border-zero

a {
  border: none; // Failing result reported
}
```

### Disable/enable all linters

```scss
// sass-lint:disable-all
p {
  border: none; // No result reported
}
// sass-lint:enable-all

a {
  border: none; // Failing result reported
}
```

---

## CLI

Sass Lint [`v1.1.0`](https://github.com/sasstools/sass-lint/releases/tag/v1.1.0) introduced the ability to run Sass Lint through a command line interface. See the [CLI Docs](https://github.com/sasstools/sass-lint/tree/master/docs/cli) for full documentation on how to use the CLI.

There are small differences which are useful to understand over other CLI tools you may have encountered with other linters.

By default any rule set to severity: `2` in your config will throw an error which will stop the CLI on the first error it encounters. If you wish to see a list of errors and not have the CLI exit then you'll need to use the `-q` or `--no-exit` flag.

Warnings or any rule set to severity: `1` in your config by default will not be reported by the CLI tool unless you use verbose flag `-v` or `--verbose`.

With this in mind if you would like to have the CLI show both warnings and errors then at the very least your starting point to use the cli should be the following command.
`sass-lint -v -q`

### CLI Examples

#### Specify a config

Below is an example of the command being used to load a config `-c app/config/.sass-lint.yml` file, show errors and warnings on the command line, and target a glob pattern `**/*.scss`:

```
sass-lint -c app/config/.sass-lint.yml '**/*.scss' -v -q
```

or with long form flags

```
sass-lint --config app/config/.sass-lint.yml '**/*.scss' --verbose --no-exit
```

#### Including multiple source destinations
By default when specifying a directory/file to lint from the CLI you would do something similar to the following

```
sass-lint 'myapp/**/*.scss' -v -q
```

or with long form flags

```
sass-lint 'myapp/**/*.scss' --verbose --no-exit
```
> Notice that you need to wrap glob patterns in quotation marks

If you want to specify multiple input sources then you need to include a single comma and a space `, ` to separate each pattern as shown in the following
```
sass-lint 'myapp/dir1/**.*.scss, myapp/dir2/**/*.scss' -v -q
```

or with long form flags

```
sass-lint 'myapp/dir1/**.*.scss, myapp/dir2/**/*.scss' --verbose --no-exit
```

If you don't include the extra space after the comma then the multiple patterns will not be interpreted correctly and you could see `sass-lint` fail.

#### Ignore files/patterns
To add a list of files to ignore `tests/**/*.scss, dist/other.scss` into the mix you could do the following:
```
sass-lint -c app/config/.sass-lint.yml '**/*.scss' -v -q -i 'tests/**/*.scss, dist/other.scss'
```
or with long form flags
```
sass-lint --config app/config/.sass-lint.yml '**/*.scss' --verbose --no-exit --ignore 'tests/**/*.scss, dist/other.scss'
```


> Notice that glob patterns need to be wrapped in quotation or single quote marks in order to be passed to sass-lint correctly and if you want to ignore multiple paths you also need to wrap it in quotation marks and separate each pattern/file with a comma and a space `, `.

This will be revisited and updated in `sass-lint` v2.0.0.

For further information you can visit our CLI documentation linked below.

### [CLI Documentation](https://github.com/sasstools/sass-lint/tree/master/docs/cli)

---

## Front matter

Certain static site generators such as [Jekyll](http://jekyllrb.com/docs/frontmatter/) include the YAML front matter block at the top of their scss file. Sass-lint by default checks a file for this block and attempts to parse your Sass without this front matter. You can see an example of a front matter block below.

```scss

---
# Only the main Sass file needs front matter (the dashes are enough)
---

.test {
  color: red;
}

```

---

## Contributions

We welcome all contributions to this project but please do read our [contribution guidelines](https://github.com/sasstools/sass-lint/blob/master/CONTRIBUTING.md) first, especially before opening a pull request. It would also be good to read our [code of conduct](https://github.com/sasstools/sass-lint/blob/master/CODE_OF_CONDUCT.md).

Please don't feel hurt or embarrassed if you find your issues/PR's that don't follow these guidelines closed as it can be a very time consuming process managing the quantity of issues and PR's we receive. If you have any questions just ask!

---

## Creating Rules

Our AST is [Gonzales-PE](https://github.com/tonyganch/gonzales-pe/tree/dev). Each rule will be passed the full AST which they can traverse as they please. There are many different [node types](https://github.com/tonyganch/gonzales-pe/blob/dev/docs/node-types.md) that may be traversed, and an extensive [API for working with nodes](https://github.com/tonyganch/gonzales-pe/tree/dev#api). The file of the rule must have the same name as the name of the rule. All of the available rules are in our [rules directory](https://github.com/sasstools/sass-lint/tree/develop/lib/rules). Default options will be merged in with user config.

---

## Task Runner Integration

* [Gulp](https://www.npmjs.com/package/gulp-sass-lint)
* [Grunt](https://github.com/sasstools/grunt-sass-lint)

## Module Bundler Integration

* [rollup.js](https://github.com/kopacki/rollup-plugin-sass-lint)

## IDE Integration

* [Atom](https://atom.io/packages/linter-sass-lint)
* [Sublime Text](https://github.com/skovhus/SublimeLinter-contrib-sass-lint)
* [Brackets](https://github.com/petetnt/brackets-sass-lint)
* [IntelliJ IDEA, RubyMine, WebStorm, PhpStorm, PyCharm](https://github.com/idok/sass-lint-plugin)
* [Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=glen-84.sass-lint)
* [Vim](https://github.com/gcorne/vim-sass-lint)
