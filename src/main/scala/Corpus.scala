
/* vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


package com.mcclure.intra
import scala.collection.mutable.ArrayBuffer
import scala.collection.mutable.HashMap


class Corpus {


  val texts = ArrayBuffer[Text]()
  var typeCounts = HashMap[String, Int]()
  var typeScores = HashMap[String, Int]()


  /** Add a new text to the corpus and update the type counts / scores.
    * TODO|dev
    *
    * @param text The new text.
    */
  def addText(text: Text) {

    // Register the text.
    texts += text

    // Update the corpus-wide type counts.
    typeCounts ++ text.typeWordOffsets.map {
      case (k, v) => k -> (v.length + typeCounts.getOrElse(k, 0))
    }

  }


}
