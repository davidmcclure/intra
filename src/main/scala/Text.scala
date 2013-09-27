
/* vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


package com.mcclure.intra
import scala.collection.mutable.ArrayBuffer


class Text(val text: String) {

  val tokens = ArrayBuffer[Tuple2[String, Int]]()

  def tokenize {

    var charOffset = 0
    var tokenCount = 0
    var token = ""

    // Walk the characters in the text.
    for ((char, index) <- text.zipWithIndex) {

      // If the character is a letter, add it to the current token. If we're
      // at the left boundary of a new token, store the character offset.

      if (char.isLetter) {
        if (token == "") charOffset = index
        token += char
      }

      // If a non-empty token has been accumulated and either (a) the current
      // character isn't a letter, meaning we're at the end of a word, or (b)
      // we're at the last character in the text, store the token / character
      // offset and clear the running token.

      if (token != "" && (!char.isLetter || index+1 == text.length)) {
        tokens += Tuple2(token, index)
        token = ""
      }

    }

  }

}
