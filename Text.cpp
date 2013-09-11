
/* vim: set tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


#include "Text.h"

using namespace std;


/**
 * Store the raw text string and text length, tokenize the text.
 * @param string text: The raw text.
 */
Text::Text( string text ) : text( text )
{
  tokenize( );
}


/**
 * Store the raw text string, tokenize the text.
 */
void Text::tokenize( )
{

  int charOffset = 0;
  int tokenCount = 0;
  string word = "";

  for( int i = 0; i < text.size( ); ++i ) {

    char c = text[i];
    bool isLetter = isalpha( c );

    if( isLetter ) {
      if( word == "" ) charOffset = i;
      word += c;
    }

    if( word != "" && ( !isLetter || i+1 == text.size( ) ) ) {
      positions[word].push_back( tokenCount++ );
      tokens.push_back( make_pair( word, charOffset ) );
      word = "";
    }

  }

}
