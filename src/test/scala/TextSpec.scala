
/* vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


package com.mcclure.intra
import scala.collection.mutable.ArrayBuffer
import scala.collection.mutable.HashMap
import org.scalatest._


class TextSpec extends WordSpec with Matchers {

  "A Text" when {

    "instantiated" should {

      "tokenize immediately by default" in {

        val text = new Text("text")

        text.tokens should not be (null)
        text.types should not be (null)

      }

      "not tokenize immediately when `tokenizeNow` is false" in {

        val text = new Text("text", false)

        text.tokens should be (null)
        text.types should be (null)

      }

    }

    "tokenized" should {

      "record tokens -> character offsets" in {

        val text = new Text("aa bb cc")

        text.tokens should equal (ArrayBuffer(
          ("aa", 0),
          ("bb", 3),
          ("cc", 6)
        ))

      }

      "record types -> word offsets" in {

        val text = new Text("a b c a b c a b c")

        text.types should equal (HashMap(
          "a" -> ArrayBuffer(0, 3, 6),
          "b" -> ArrayBuffer(1, 4, 7),
          "c" -> ArrayBuffer(2, 5, 8)
        ))

      }

      "ignore non-letter characters" in {

        val text = new Text("a 1 b & c @")

        text.tokens should equal (ArrayBuffer(
          ("a", 0),
          ("b", 4),
          ("c", 8)
        ))

        text.types should equal (HashMap(
          "a" -> ArrayBuffer(0),
          "b" -> ArrayBuffer(1),
          "c" -> ArrayBuffer(2)
        ))

      }

    }

  }

}
