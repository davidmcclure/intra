
/* vim: set expandtab tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


package com.mcclure.intra


class PorterStemmer(val token: String) {


  private var _token = token


  /** Stem the token 
    */
  def stem: String = {

    if (_token.length < 3) return _token

    step1a
    step1b
    step1c
    step2
    step3
    step4
    step5

    _token

  }


  /** Step 1a.
    */
  protected def step1a {
    // TODO
  }


  /** Step 1b.
    */
  protected def step1b {
    // TODO
  }


  /** Step 1c.
    */
  protected def step1c {
    // TODO
  }


  /** Step 2.
    */
  protected def step2 {
    // TODO
  }


  /** Step 3.
    */
  protected def step3 {
    // TODO
  }


  /** Step 4.
    */
  protected def step4 {
    // TODO
  }


  /** Step 5.
    */
  protected def step5 {
    // TODO
  }


}
