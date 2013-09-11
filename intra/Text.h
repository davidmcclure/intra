
/* vim: set tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


#ifndef TEXT_H
#define TEXT_H

#include <string>
using namespace std;


class Text
{

  public:

    Text( string text );
    string text;

  private:

    void tokenize( );

};


#endif
