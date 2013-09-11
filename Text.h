
/* vim: set tabstop=2 shiftwidth=2 softtabstop=2 cc=80; */


#ifndef TEXT_H
#define TEXT_H

#include <string>
#include <vector>
#include <tr1/unordered_map>

using namespace std;


class Text
{

  public:

    Text( string text );

  private:

    void tokenize( );
    string text;

    tr1::unordered_map<string, vector<int> > positions;
    vector<pair<string, int> > tokens;

};


#endif
