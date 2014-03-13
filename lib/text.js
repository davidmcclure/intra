
/* vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


/*
 * Initialize the token and type containers.
 *
 * @param {String} text: The raw text.
 * @param {Boolean} tokenizeNow: If true, tokenize immediately.
 */
var Text = function(text, tokenizeNow) {

  this.text = text;
  this.tokens = [];

}
