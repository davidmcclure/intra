
/* vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


package com.mcclure.intra
import scala.collection.mutable.ArrayBuffer
import scala.collection.mutable.HashMap


class Text(val text: String) {


  val tokens = ArrayBuffer[Tuple2[String, Int]]()
  val positions = HashMap[String, ArrayBuffer[Int]]()


  def tokenize {

    var token = ""
    var start = 0
    var count = 0

    for ((c, i) <- text.zipWithIndex) {

      // If the character is a letter, add it to the current token. If we're
      // at the left boundary of a new token, store the character offset.

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
        tokens += Tuple2(token, start)
        positions.getOrElseUpdate(token, ArrayBuffer[Int]()) += count

        count += 1
        token = ""

      }

    }

  }


}
