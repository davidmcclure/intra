
/* vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


package com.mcclure.intra
import scala.collection.mutable.ArrayBuffer
import scala.collection.mutable.HashMap


/** An individual text in a corpus.
  *
  * @constructor Create a text from a string.
  * @param text The raw string value.
  * @param tokenizeNow If true, tokenize the text immediately.
  */
class Text(val text: String, tokenizeNow: Boolean = true) {


  var tokenCharacterOffsets: ArrayBuffer[Tuple2[String, Int]] = null
  var typeWordOffsets: HashMap[String, ArrayBuffer[Int]] = null

  if (tokenizeNow) tokenize


  /** Tokenize the text. For each token, keep track of the starting character
    * offset in the original text. For each type, keep track of the collection
    * of offsets at which the type appears.
    */
  def tokenize {

    tokenCharacterOffsets = ArrayBuffer[Tuple2[String, Int]]()
    typeWordOffsets = HashMap[String, ArrayBuffer[Int]]()

    var token = ""
    var start = 0
    var count = 0

    for ((c, i) <- text.zipWithIndex) {

      // If the character is a letter, add it to the current token. If we're
      // at the left boundary of a new token, store the starting offset.

      if (c.isLetter) {
        if (token == "") start = i
        token += c
      }

      // If a non-empty token has been accumulated and either (a) the current
      // character isn't a letter, meaning we've reached the end of a word, or
      // (b) we're at the last character in the text, store the token with its
      // character offset and clear the running token.

      if (token != "" && (!c.isLetter || i+1 == text.length)) {

        // Register the new token.
        tokenCharacterOffsets += Tuple2(token, start)
        typeWordOffsets.getOrElseUpdate(token, ArrayBuffer[Int]()) += count

        count += 1
        token = ""

      }

    }

  }


}
