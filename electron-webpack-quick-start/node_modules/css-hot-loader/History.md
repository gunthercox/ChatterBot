### 1.4.4 2019-03-13

- fix: replace DOM api remove to removeChild, support ie [!57](https://github.com/shepherdwind/css-hot-loader/pull/57)

### 1.4.3 2018-12-12

- feat: replace appendChild by insertBefore by [@focus7eleven](https://github.com/focus7eleven) [#54](https://github.com/shepherdwind/css-hot-loader/pull/54)

### 1.4.2 2018-08-15

- feat: add cssModule option [!51](https://github.com/shepherdwind/css-hot-loader/pull/51)

### 1.4.1 2018-07-26

- fix: css module reload issue [#47](https://github.com/shepherdwind/css-hot-loader/pull/47) fix by [@keegan-lillo](https://github.com/keegan-lillo)

### 1.4.0 2018-07-11

- feat: support `reloadAll` config, support code split issue [#44](https://github.com/shepherdwind/css-hot-loader/issues/44)

### 1.3.9 2018-03-27

- fix: Webpack 4 compatibility fix by @vagusX [!39](https://github.com/shepherdwind/css-hot-loader/pull/39)

### 1.3.8 2018-03-01

- feat: using debounce for update in DOM by @53c701d [!35](https://github.com/shepherdwind/css-hot-loader/pull/35)

### 1.3.7 / 2018-02-10

- Fix issue causing multiple instances of link tags to be inserted by @aminland [!33](https://github.com/shepherdwind/css-hot-loader/pull/33)

### 1.3.6 / 2018-01-23

- Safe access to 'src' of the last "script" tag[#30](https://github.com/shepherdwind/css-hot-loader/pull/30)

### 1.3.5 / 2017-12-24

- Refactor hotModuleReplacement [#27](https://github.com/shepherdwind/css-hot-loader/pull/27) by @GeorgeTaveras1231

### 1.3.3 / 2017-11-08

- Replace css link instead of adding new one [#24](https://github.com/shepherdwind/css-hot-loader/pull/24)

### 1.3.2 / 2017-10-07

- memory leak fix, only reload css files [#22](https://github.com/shepherdwind/css-hot-loader/pull/22) by @nickaversano

### 1.3.1 / 2017-09-04

- Use var instead of const for IE10 [#17](https://github.com/shepherdwind/css-hot-loader/pull/17)

### 1.3.0 / 2017-07-03

- Add support for commons chunk [#12](https://github.com/shepherdwind/css-hot-loader/pull/12) by @tfoxy
- Fix error when use a local host [#11](https://github.com/shepherdwind/css-hot-loader/pull/11) by @tfoxy

### 1.2.0 / 2017-06-23

- Applying styles without site jerking [!9](https://github.com/shepherdwind/css-hot-loader/pull/9) by @nvlad

### 1.1.1 / 2017-05-18

- Use loaderUtils.stringifyRequest to fix error path on windows [!6](https://github.com/shepherdwind/css-hot-loader/pull/6) by @dannsam

### 1.1.0 / 2017-05-14

- Add option fileMap, fix [#3](https://github.com/shepherdwind/css-hot-loader/issues/3)

### 1.0.3 / 2017-05-05

- IE11 compatibility [!2](https://github.com/shepherdwind/css-hot-loader/pull/2)
by @extronics

### 1.0.2 / 2017-04-05

- css file change md5 hash , support webpack 2.0, fix issue [#1](https://github.com/shepherdwind/css-hot-loader/issues/1)

### 1.0.1 / 2017-01-26

- First version, work fine
