
/* vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


package com.mcclure.intra
import org.scalatest._


class TextSpec extends WordSpec with Matchers {

  "A Text" when {

    "instantiated" should {

      "tokenize immediately by default" in {
        val text = new Text("text")
        text.tokenCharacterOffsets should not be (null)
        text.typeWordOffsets should not be (null)
      }

      "not tokenize immediately when `tokenizeNow` is false" in {
        val text = new Text("text", false)
        text.tokenCharacterOffsets should be (null)
        text.typeWordOffsets should be (null)
      }

    }

    "tokenized" should {

      "populate token character offsets" in {
        val text = new Text("1 2 3")
        text.tokenCharacterOffsets(0)._1 should equal ("1")
        text.tokenCharacterOffsets(0)._2 should equal (0)
        text.tokenCharacterOffsets(1)._1 should equal ("2")
        text.tokenCharacterOffsets(1)._2 should equal (3)
        text.tokenCharacterOffsets(2)._1 should equal ("3")
        text.tokenCharacterOffsets(2)._2 should equal (6)
      }

      "populate type word offsets" in {
        val text = new Text("1 2 3 1 2 3 1 2 3")
        // TODO
      }

    }

  }

}
