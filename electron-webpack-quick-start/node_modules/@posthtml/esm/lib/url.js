const URL = /^\w+:\/\//

const ATTRS = [
  {
    attrs: { src: true }
  },
  {
    attrs: { href: true }
  },
  {
    attrs: { srcset: true }
  }
]

const filter = (url, options) => {
  if (URL.test(url)) {
    return true
  }

  if (url.startsWith('//')) {
    return true
  }

  if (options.url instanceof RegExp) {
    return options.url.test(url)
  }

  if (typeof options.url === 'function') {
    return options.url(url)
  }

  return false
}

/**
 * HTML URL Plugin
 *
 * @method urls
 *
 * @param  {Object} [options={}] Plugin Options
 *
 * @return {Array} tree  PostHTML AST
 */
function plugin (options = {}) {
  return function (tree) {
    let idx = 0

    tree.match(ATTRS, (node) => {
      // <tag src="path/to/file.ext">
      if (node.attrs.src) {
        // Ignore <import>/<include
        if (node.tag === 'import' || node.tag === 'include') {
          return node
        }

        // Ignore external && filtered URLs
        if (filter(node.attrs.src, options)) {
          return node
        }

        // Add HTML URL to result.messages
        tree.messages.push({
          type: 'import',
          plugin: '@posthtml/esm',
          url: node.attrs.src,
          name: `HTML__URL__${idx}`,
          import () {
            return `import ${this.name} from '${this.url}';\n`
          }
        })

        // Add content placeholders to HTML
        node.attrs.src = '${' + `HTML__URL__${idx}` + '}'

        idx++

        return node
      }

      // <tag href="path/to/file.ext">
      if (node.attrs.href) {
        // Ignore external && filtered URLs
        if (filter(node.attrs.href, options)) {
          return node
        }

        // Add HTML URL to result.messages
        tree.messages.push({
          type: 'import',
          plugin: '@posthtml/esm (URL)',
          url: node.attrs.href,
          name: `HTML__URL__${idx}`,
          import () {
            return `import ${this.name} from '${this.url}';\n`
          }
        })

        // Add content placeholder to HTML
        node.attrs.href = '${' + `HTML__URL__${idx}` + '}'

        idx++

        return node
      }
      // <tag srcset="path/to/file.ext">
      if (node.attrs.srcset) {
        // Ignore external && filtered URLs
        if (filter(node.attrs.srcset, options)) {
          return node
        }

        // Add HTML URL to result.messages
        tree.messages.push({
          type: 'import',
          plugin: '@posthtml/esm (URL)',
          url: node.attrs.srcset,
          name: `HTML__URL__${idx}`,
          import () {
            return `import ${this.name} from '${this.url}';\n`
          }
        })

        // Add content placeholder to HTML
        node.attrs.srcset = '${' + `HTML__URL__${idx}` + '}'

        idx++

        return node
      }
    })

    return tree
  }
}

/**
 * ESM URL Plugin (`HTML__URL`)
 *
 * @module url
 * @version 1.0.0
 * @license MIT
 */
module.exports = plugin
