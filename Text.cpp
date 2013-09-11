
/* vim: set tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


#include <iostream>
#include "Text.h"
using namespace std;


/**
 * Store the raw text string and text length, tokenize the text.
 * @param string text: The raw text.
 */
Text::Text( string text ) : text( text )
{
  length = text.size( );
  tokenize( );
}


/**
 * Store the raw text string, tokenize the text.
 * @param string text: The raw text.
 */
void Text::tokenize( )
{

  string word = "";
  int offset = 0;

  for( int i = 0; i < length; ++i ) {

    char c = text[i];

    // Is the character a letter?
    bool is_letter = isalpha( c );

    if( is_letter ) {
      if( word == "" ) offset = i;
      word += c;
    }

    if( word != "" && ( !is_letter || i+1 == length ) ) {
      // TODO: Stem the word, store offset.
      cout << word << " " << offset;
      word = "";
    }

  }

}
