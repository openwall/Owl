// +-------------------------------------------------------------------------+
// |                     Script Plus Plus vers. 0.2.15                       |
// | Copyright (c) Andrey Vikt. Stolyarov <crocodil_AT_croco.net>  2003-2007 |
// | ----------------------------------------------------------------------- |
// | This is free software.  Permission is granted to everyone to use, copy  |
// |        or modify this software under the terms and conditions of        |
// |                 GNU LESSER GENERAL PUBLIC LICENSE, v. 2.1               |
// |     as published by Free Software Foundation (see the file LGPL.txt)    |
// |                                                                         |
// | Please visit http://www.croco.net/software/scriptpp to get a fresh copy |
// | ----------------------------------------------------------------------- |
// |   This code is provided strictly and exclusively on the "AS IS" basis.  |
// | !!! THERE IS NO WARRANTY OF ANY KIND, NEITHER EXPRESSED NOR IMPLIED !!! |
// +-------------------------------------------------------------------------+




#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <ctype.h>

#include "scrvar.hpp"


const int size_of_memblock_header = 8;

struct ScriptVariableImplementation {
    int refcount;
    int maxlen;  // buf[maxlen] may still be accessed but is always 0
    char buf[1];
};

static ScriptVariableImplementation TheEmptyString = { 1, 0, "" };


ScriptVariable::ScriptVariable()
{
    p = 0;
    Assign(&TheEmptyString);
}

ScriptVariable::ScriptVariable(int len)
{
    p = 0;
    Create(len);
    p->buf[0] = 0;
}

ScriptVariable::ScriptVariable(const char *str)
{
    p = 0;
    int len = strlen(str);
    Create(len);
    memcpy(p->buf, str, len);
}

ScriptVariable::ScriptVariable(int len, const char *format, ...)
{
    p = 0;
    /* the following code is shamelessly stolen from man (3) vsnprintf */
    while (1) {
        Create(len);
         /* Try to print in the allocated space. */
	va_list ap;
        va_start(ap, format);
        int n = vsnprintf (p->buf, len, format, ap);
        va_end(ap);
        /* If that worked, we're done */
        if (n > -1 && n < len)
            break;
        /* Else try again with more space. */
        if (n > -1)    /* glibc 2.1 */
            len = n+1; /* precisely what is needed */
        else           /* glibc 2.0 */
            len *= 2;  /* twice the old size */
    }
}

ScriptVariable::ScriptVariable(const ScriptVariable& other)
{
    p = 0;
    Assign(other.p);
}

ScriptVariable::~ScriptVariable()
{
    Unlink();
}

void ScriptVariable::Unlink()
{
    if(p) {
        if(--(p->refcount)<=0) free(p);
        p = 0;
    }
}

void ScriptVariable::Assign(ScriptVariableImplementation *q)
{
    Unlink();
    p = q;
    p->refcount++;
}

void ScriptVariable::Create(int len)
{
    Unlink();
    int efflen = 16;
    int hdrsize = sizeof(ScriptVariableImplementation)
                  + size_of_memblock_header;
		  // memblock is for optim.
    int minsize = hdrsize + len;
    while(efflen < minsize) efflen *= 2;
    p = reinterpret_cast<ScriptVariableImplementation*>
               (malloc(efflen - size_of_memblock_header));
    p->refcount = 1;
    p->maxlen = efflen - hdrsize;
    p->buf[len] = 0;
}

void ScriptVariable::EnsureOwnCopy()
{
    if(p && p->refcount > 1) {
        int len = Length();
        ScriptVariableImplementation *tmp = p;
        Create(len);
        memcpy(p->buf, tmp->buf, len);
    }
}

int ScriptVariable::Length() const
{
    if(p) return strlen(p->buf);
    else return 0;
}

const char *ScriptVariable::c_str() const
{
    if(!p) return "";
    return p->buf;
}

char ScriptVariable::operator[](int i) const
{
    return p->buf[i];
}

char& ScriptVariable::operator[](int i)
{
    EnsureOwnCopy();
    return p->buf[i];
}

////////////////////////////////////////

ScriptVariable ScriptVariable::operator+(const char *o2) const
{
    int len1 = Length();
    int len2 = strlen(o2);
    int newlen = len1 + len2;
    ScriptVariable res(newlen);
    memcpy(res.p->buf, p->buf, len1);
    memcpy(res.p->buf+len1, o2, len2);
    res.p->buf[newlen] = 0;
    return res;
}

ScriptVariable& ScriptVariable::operator+=(const char *o2)
{
    int len1 = Length();
    int len2 = strlen(o2);
    int newlen = len1 + len2;
    if(p && p->refcount == 1 && p->maxlen >= newlen) {
        // in this special case we can just copy the second string in
        memcpy(p->buf+len1, o2, len2);
        p->buf[newlen] = 0;
    } else {
        // we have to create another one, so let's just make it sum...
	ScriptVariable res(*this + o2);
        Assign(res.p);
    }
    return *this;
}

ScriptVariable& ScriptVariable::operator=(const char *o2)
{
    int len2 = strlen(o2);
    Create(len2);
    memcpy(p->buf, o2, len2 + 1);
    return *this;
}

///////////////////////////

ScriptVariable ScriptVariable::operator+(char c) const
{
    char bb[2];
    bb[0]=c; bb[1]=0;
    return (*this)+bb;
}

ScriptVariable& ScriptVariable::operator+=(char c)
{
    char bb[2];
    bb[0]=c; bb[1]=0;
    return (*this)+=bb;
}

ScriptVariable& ScriptVariable::operator=(char c)
{
    char bb[2];
    bb[0]=c; bb[1]=0;
    return (*this)=bb;
}

///////////////////////////////////////////

ScriptVariable ScriptVariable::operator+(const ScriptVariable &o2) const
{
    return (*this) + o2.p->buf;
}

ScriptVariable& ScriptVariable::operator+=(const ScriptVariable &o2)
{
    (*this) += o2.p->buf;
    return *this;
}

ScriptVariable& ScriptVariable::operator=(const ScriptVariable &o2)
{
    Assign(o2.p);
    return *this;
}


const ScriptVariable& ScriptVariable::Toupper()
{
    EnsureOwnCopy();
    int len = Length();
    for(int i=0; i<len; i++)
        p->buf[i] = toupper(p->buf[i]);
    return *this;
}

const ScriptVariable& ScriptVariable::Tolower()
{
    EnsureOwnCopy();
    int len = Length();
    for(int i=0; i<len; i++)
        p->buf[i] = tolower(p->buf[i]);
    return *this;
}

int ScriptVariable::Strcmp(const ScriptVariable &o2) const
{
    return strcmp(p->buf, o2.p->buf);
}

int ScriptVariable::Strcasecmp(const ScriptVariable &o2) const
{
    return strcasecmp(p->buf, o2.p->buf);
}

bool ScriptVariable::HasPrefix(const char *pr) const
{
    for(const char *qq = p->buf; *pr; pr++, qq++)
        if(*pr!=*qq) return false;
    return true;
}

bool ScriptVariable::HasPrefix(const ScriptVariable& prefix) const
{
    return HasPrefix(prefix.c_str());
}

bool ScriptVariable::HasSuffix(const char *suf) const
{
    int suflen = strlen(suf);
    for(const char *qq = p->buf + Length() - suflen; *suf; suf++, qq++)
        if(*suf!=*qq) return false;
    return true;
}

bool ScriptVariable::HasSuffix(const ScriptVariable& suffix) const
{
    int l = suffix.Length();
    return (*const_cast<ScriptVariable*>(this)).Range(-l, l).Get() == suffix;
}

void ScriptVariable::Trim(const char *spaces)
{
    (*this) = Whole().Trim(spaces).Get();
}


ScriptVariable::Substring::
Substring(ScriptVariable &a_master, int a_pos, int a_len)
{
    master = &a_master;
    pos = a_pos>=0 ? a_pos : (master->Length() + a_pos);
    if(pos<0) pos = 0;
    len = a_len;
    if(len == -1) {
        len = master->Length() - pos;
    }
    if(pos+len > master->p->maxlen) {
        len = master->p->maxlen - pos;
    }
}

void ScriptVariable::Substring::Erase()
{
    master->EnsureOwnCopy();
    for(char *p = master->p->buf + pos; ; p++) {
        if(!*p) { // this means it was really shorter than len
           *(master->p->buf + pos) = 0;
           break;
        }
        if(!(*p = *(p+len))) {
           break;
        }
    }
    len = 0;
}

void ScriptVariable::Substring::Replace(const char *what)
{
    master->EnsureOwnCopy();
    int mlen = master->Length();
    if(pos+len > mlen)
        len = mlen - pos;
    int whatlen = strlen(what);
    if(whatlen > len) { // first move the rest forward
        // do we have enough room for it?
	int delta = whatlen - len;
        if(mlen+delta <= master->p->maxlen) {
	    // yes, we've got enough room
            memmove(master->p->buf + pos + whatlen,
	            master->p->buf + pos + len,
		    mlen - pos - len + 1);
            master->p->buf[mlen+delta] = 0; // sanity
	} else {
	    // not enough room, don't bother moving
            ScriptVariable tmp(mlen+delta);
	    memmove(tmp.p->buf, master->p->buf, pos);
	    memmove(tmp.p->buf+whatlen, master->p->buf+len,
		    mlen - pos - len + 1);
            (*master) = tmp;
        }
    } else
    if(whatlen < len) { // first move the rest backward
        memmove(master->p->buf + pos + whatlen,
                master->p->buf + pos + len,
                mlen - pos - len + 1);
    }
    // now just replace
    memcpy(master->p->buf + pos, what, whatlen);
    len = whatlen;
}

ScriptVariable ScriptVariable::Substring::Get() const
{
    int llen = len>=0 ? len : master->Length()-pos;
    if(llen<=0) {
        return ScriptVariable("");
    }
    ScriptVariable res(llen);
    memcpy(res.p->buf, master->p->buf + pos, llen);
    res.p->buf[llen] = 0;
    return res;
}

bool ScriptVariable::Substring::FetchWord(Substring &word, const char *spaces)
{
    char *p = master->p->buf + pos;
    char *q = p;
    while(*p && strchr(spaces, *p)) p++;
    if(!*p) return false;

    word.master = master;
    word.pos = pos + (p-q); // skip spaces

    q = p;
    while(*p && !strchr(spaces, *p)) p++;
    word.len = p-q;

    int fetchedlen = word.pos + word.len - pos;
    pos += fetchedlen;
    len -= fetchedlen;

    return true;
}

bool ScriptVariable::Substring::
FetchToken(Substring &token,
           const char *delimiters,
           const char *trim_spaces)
{
    if(len<0) // this means nothing left in the string
        return false;
              // else, at least one token exists
    char *p = master->p->buf + pos;
    token.master = master;
    token.pos = pos;

    char *q = p;

    while(*p && !strchr(delimiters, *p)) p++;

    if(*p) {
        // delimiter found; there will be another token...
        token.len = (p-q);
        pos += p-q+1;
        len -= p-q+1;
    } else {
        // no delimiters; this will be the last and the only token
        token.len = len;
        pos += len;
        len = -1; // no more tokens!
    }

    if(trim_spaces && *trim_spaces) token.Trim(trim_spaces);

    return true;
}

ScriptVariable::Substring
ScriptVariable::Substring::FetchWord(const char *spaces)
{
    Substring ret;
    FetchWord(ret, spaces);
    return ret;
}

ScriptVariable::Substring ScriptVariable::Substring::
FetchToken(const char *delimiters, const char *trim_spaces)
{
    Substring ret;
    FetchToken(ret, delimiters, trim_spaces);
    return ret;
}

void ScriptVariable::Substring::Move(int d)
{
    pos+=d;
    if(pos < 0) pos = 0;
    if(pos >= master->p->maxlen) pos = master->p->maxlen-1;
    if(pos+len > master->p->maxlen) len = master->p->maxlen - pos;
}

void ScriptVariable::Substring::Resize(int d)
{
    len+=d;
    if(len<0)
        len = 0;
    else if(pos+len > master->p->maxlen)
        len = master->p->maxlen - pos;
}

void ScriptVariable::Substring::ExtendToBegin()
{
    len += pos;
    pos = 0;
}

void ScriptVariable::Substring::ExtendToEnd()
{
    len = master->Length() - pos;
}

const ScriptVariable::Substring&
ScriptVariable::Substring::Trim(const char *spaces)
{
    char *p = master->p->buf + pos;
    char *q = p;
    while(*p && strchr(spaces, *p)) p++;
    pos+=(p-q);
    len-=(p-q);
    q=p;
    p+=len-1;
    while(p>q && strchr(spaces, *p)) p--;
    len = p-q+1;
    return *this;
}

ScriptVariable::Substring ScriptVariable::Strchr(int c)
{
    const char *p = strchr(c_str(), c);
    if(!p) return ScriptVariable::Substring(); // invalid
    return ScriptVariable::Substring(*this, p-c_str(), 1);
}

ScriptVariable::Substring ScriptVariable::Strrchr(int c)
{
    const char *p = strrchr(c_str(), c);
    if(!p) return ScriptVariable::Substring(); // invalid
    return ScriptVariable::Substring(*this, p-c_str(), 1);
}

ScriptVariable::Substring ScriptVariable::Strstr(const char *str)
{
    const char *p = strstr(c_str(), str);
    if(!p) return ScriptVariable::Substring(); // invalid
    return ScriptVariable::Substring(*this, p-c_str(), strlen(str));
}

ScriptVariable::Substring ScriptVariable::Strrstr(const char *str)
{
    // NOT IMPLEMENTED YET!!!
    return ScriptVariable::Substring(); // invalid
}






bool ScriptVariable::Iterator::NextWord(const char *spaces)
{
    pos += len; // begin from the next position
    char *p = master->p->buf + pos;
    char *q = p;
    while(*p && strchr(spaces, *p)) p++;
    if(!*p) return false;
    pos += p - q;
    q = p;
    while(*p && !strchr(spaces, *p)) p++;
    len = p - q;
    just_started = false; // this is just to keep the things consistent
                    // NextWord doesn't really use the just_started variable
    return true;
}

bool ScriptVariable::Iterator::NextToken(
                  const char *delimiters,
	          const char *trim_spaces)
{
    char *p, *q;
    if(!just_started) { // not the starting situation
              // we need first to find the delimiter that finishes the
	      // current token, and only in this case
        pos += len; // begin from the next position
        p = master->p->buf + pos;
        q = p;
        while(*p && !strchr(delimiters, *p)) p++;
        if(!*p) return false; // that was the last token
	p++;
	pos += p - q; // now pos is the next position after the delimiter
    } else {
        p = master->p->buf;  // begin from the beginning
        just_started = false;
    }
    q = p;
    while(*p && !strchr(delimiters, *p)) p++;
    p--;
    // q points at the begin and p points at the end
    if(trim_spaces && *trim_spaces) {
        // need trimming
        while(q<=p && strchr(trim_spaces, *q)) q++;
        if(q<=p) while(strchr(trim_spaces, *p)) p--;
	// if everything gets trim away, then p is actually less than q
    }
    pos = q - master->p->buf;
    len = p - q + 1;
    //return (len + pos > 0); // to prevent infinite loop on, say, empty string
    return true;
}



bool ScriptVariable::Iterator::PrevWord(const char *spaces)
{
    if(just_started) { pos = master->Length(); }
    pos -= 1; // begin from the previous position
    char *limit = master->p->buf;
    char *p = limit + pos;
    while(p>=limit && strchr(spaces, *p)) p--;
    if(p<limit) return false;
    char *q = p;
    while(p>=limit && !strchr(spaces, *p)) p--;
    pos = p - limit + 1;
    len = q - p;
    just_started = false;
    return true;
}

bool ScriptVariable::Iterator::PrevToken(
                  const char *delimiters,
	          const char *trim_spaces)
{
    char *p, *q;
    char *limit = master->p->buf;
    if(!just_started) { // not the starting situation
              // we need first to find the delimiter that starts the
	      // current token, and only in this case
        pos -= 1; // begin from the previous position
        p = limit + pos;
        q = p;
        while(p>=limit && !strchr(delimiters, *p)) p--;
        if(p<limit) return false; // that was the first token
	p--; // jump over the delimiter
	pos -= p - q; // now pos is the next position before the delimiter
    } else {
        p = limit + master->Length() - 1;  // begin from the end
        just_started = false;
    }
    q = p;
    while(p>=limit && !strchr(delimiters, *p)) p--;
    p++;
    // q points at the end and p points at the begin
    if(trim_spaces && *trim_spaces) {
        // need trimming
        while(q>=p && strchr(trim_spaces, *q)) q--;
        while(q>p && strchr(trim_spaces, *p)) p++;
	// if everything gets trim away, then q is actually less than p
    }
    pos = p - limit;
    len = q - p + 1;
    return true;
}


ScriptVariable::BadNumber::BadNumber(const ScriptVariable &v)
{
    var = new ScriptVariable(v);
}

ScriptVariable::BadNumber::BadNumber(const BadNumber &b)
{
    var = new ScriptVariable(*(b.var));
}

ScriptVariable::BadNumber::~BadNumber()
{
    delete var;
}

bool ScriptVariable::GetLong(long &l) const throw ()
{
    long ret;
    char *err;
    char *q = p->buf;
    ret = strtol(q, &err, 0);
    if(*q != '\0' && *err == '\0') {
        l = ret;
        return true;
    } else {
        return false;
    }
}

bool ScriptVariable::GetDouble(double &d) const throw ()
{
    double ret;
    char *err;
    char *q = p->buf;
    ret = strtod(q, &err);
    if(*q != '\0' && *err == '\0') {
        d = ret;
        return true;
    } else {
        return false;
    }
}

long ScriptVariable::GetLong() const throw (ScriptVariable::BadNumber)
{
    long ret;
    if(GetLong(ret))
        return ret;
    else
        throw BadNumber(*this);
}

double ScriptVariable::GetDouble() const throw (ScriptVariable::BadNumber)
{
    double ret;
    if(GetDouble(ret))
        return ret;
    else
        throw BadNumber(*this);
}

bool ScriptVariable::GetRational(long &n, long &m, bool t_b) const
                                   throw (ScriptVariable::BadNumber)
{
    long ret;
    char *err;
    char *q = p->buf;
    ret = strtol(q, &err, 10);
    if(*q == '\0' || (*err != '\0' && *err != '.')) {
        if(t_b)
            throw BadNumber(*this);
        else
            return false;
    }
    if(*err=='\0' || *(err+1)=='\0') {
         // no decimal dot or nothing right after the decimal dot
        n = ret;
        m = 1;
        return true;
    }
    // decimal dot found
    q = err+1;
    long ret2 = strtol(q, &err, 10);
    if(*err != '\0' || ret2<=0) {
        if(t_b)
            throw BadNumber(*this);
        else
            return false;
    }
    long x = 10;
    while(x<=ret2) x*=10;
    n = ret * x + ret2;
    m = x;
    return true;
}
