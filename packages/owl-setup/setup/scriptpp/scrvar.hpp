// +-------------------------------------------------------------------------+
// |                     Script Plus Plus vers. 0.2.12                       |
// | Copyright (c) Andrey Vikt. Stolyarov <crocodil_AT_croco.net>  2003-2005 |
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




#ifndef SCRVAR_HPP_SENTRY
#define SCRVAR_HPP_SENTRY

/*! \file scrvar.hpp
    \brief This file invents the ScriptVariable class
 */


//! Script Variable (a universal string)
/*! This class implements a common intuitive-clear notion of a string.
    In fact, it could be a good replacement for the 'standard' string class,
    and it even has some methods invented for compatibility reasons only.
    You shouldn't, however, expect it to be totally compatible with the
    string class; it was not the primary goal to maintain such a compatibility.
   \par
    The copy-on-write technology is well implemented. The class itself has
    only one data member (a pointer) so it is Ok to pass ScriptVariable
    objects by value.
   \par
    The main architectural difference is that the class itself doesn't have
    any methods to manipulate substrings (like erase(), replace() etc).
    Instead, there is a nested class named ScriptVariable::Substring which
    has the appropriate methods.
   \par
    The author's intention was to provide the operations which are required
    more often than the others. These are (1) various tokenization services
    (including iteration by tokens and/or by words) and (2) conversions
    to/from numbers, both floats and ints.
   \note
    There are two terms, namely word and token, which are widely used in
    this document. It is important to understand the difference. If a string
    is broken by some delimiters, and everything between any two
    delimiters is to be extracted, it is called TOKEN. For example,
    colon-separated lines such as in /etc/passwd are tokenized lines.
    If, by contrast, two items within a string can be delimited not by
    exactly one, but with any number of delimiting characters (tipically
    whitespace), then such items are called WORDS. Consider the string
    "aaa::bbb::ccc::ddd". If ":" is the only delimiter, then the string
    has 7 tokens ("aaa", "", "bbb", "", "ccc", "", "ddd") and only 4
    words ("aaa", "bbb", "ccc", "ddd").
 */
class ScriptVariable {
    struct ScriptVariableImplementation *p;
public:
        //! Default constructor
        /*! Creates an empty string */
    ScriptVariable();
        //! Constructor with an optimization hint
        /*! If you for some reason can make some estimations about how
            much space will be needed for the string, than you can pass
            a hint to the constructor so as to avoid initial resizings.
           \param len is the estimated length of your string in characters.
         */
    explicit ScriptVariable(int len);
        //! The copy constructor
        /*! \note
            The string itself is not copied until one of its users tries
            to modify it.
         */
    ScriptVariable(const ScriptVariable &other);
        //! Cast constructor
        /*! This constructor allows to create a ScriptVariable having a
            traditional C zero-terminated string.
         */
    ScriptVariable(const char *s);
        //! Sprintf constructor
        /*! Allows to create a ScriptVariable representing a result of
            processing a format string just like with sprintf(3).
            In fact, vsnprintf(3) is used to fill the string.
           \param len is a length hint. The main goal of this parameter
            is, however, just to allow to tell this constructor call from
            the ScriptVariable(const char *) one. Just pass zero len if
            you don't want to think.
           \param format is a format string. See printf(3) for the format
            string documentation.
         */
    ScriptVariable(int len, const char *format, ...);

    ~ScriptVariable();
        //! Current string length
    int Length() const;
        //! Current string length
        /*! string class compatibility name */
    int length() const { return Length(); }

        //! Convert to a traditional C string.
    const char *c_str() const;

        //! Access the particular character (read only)
    char operator[](int i) const;
        //! Access the particular character (assignment is allowed)
    char& operator[](int i);

        //! strcmp(3) functionality
    int Strcmp(const ScriptVariable &o2) const;

        //! Convert all chars to upper case.
    const ScriptVariable& Toupper();
        //! Convert all chars to lower case.
    const ScriptVariable& Tolower();

        //! Concatenation
    ScriptVariable operator+(const char *o2) const;
        //! Appending
    ScriptVariable& operator+=(const char *o2);
        //! Assignment
    ScriptVariable& operator=(const char *o2);
        //! Concatenation
    ScriptVariable operator+(char c) const;
        //! Appending
    ScriptVariable& operator+=(char c);
        //! Assignment
    ScriptVariable& operator=(char c);
        //! Concatenation
    ScriptVariable operator+(const ScriptVariable &o2) const;
        //! Appending
    ScriptVariable& operator+=(const ScriptVariable &o2);
        //! Assignment
    ScriptVariable& operator=(const ScriptVariable &o2);

    bool operator==(const ScriptVariable &o2) const
        { return Strcmp(o2) == 0; }
    bool operator!=(const ScriptVariable &o2) const
        { return Strcmp(o2) != 0; }
    bool operator<(const ScriptVariable &o2) const
        { return Strcmp(o2) < 0; }
    bool operator>(const ScriptVariable &o2) const
        { return Strcmp(o2) > 0; }
    bool operator<=(const ScriptVariable &o2) const
        { return Strcmp(o2) <= 0; }
    bool operator>=(const ScriptVariable &o2) const
        { return Strcmp(o2) >= 0; }

    bool HasPrefix(const char *prefix) const;
    bool HasPrefix(const ScriptVariable& prefix) const;

    void Trim(const char *spaces = " \t\n\r");

    class Substring {
        friend class ScriptVariable;
    protected:
        ScriptVariable *master;
	int pos;
	int len;
    public:
        Substring() : master(0), pos(0), len(-1) {}
            /*!
                 \par pos starting position; zero means the begin
                      of the string, positive value is the offset from the
                      begin, negative value is the offset from the end
                      of the string.
             */
        Substring(ScriptVariable &master, int pos=0, int len=-1);
        void Erase();
        void Replace(const char *what);
        ScriptVariable Get() const;
        char operator[](int i) const { return (*master)[i+pos]; }
        bool operator==(const Substring &o) const
            { return master == o.master && pos == o.pos && len == o.len; }

        bool FetchWord(Substring &word, const char *spaces = " \t\n\r");
	bool FetchToken(Substring &token,
                        const char *delimiters = ",",
	                const char *trim_spaces = 0);

        Substring FetchWord(const char *spaces = " \t\n\r");
	Substring FetchToken(const char *delimiters = ",",
	                     const char *trim_spaces = 0);

        void Move(int delta);
        void Resize(int delta);

           /*! Trims the substring and returns *this */
        const Substring& Trim(const char *spaces = " \t\n\r");

        const ScriptVariable& Master() const { return *master; }
        int Index() const { return pos; }
        int Length() const { return len; }

        bool Valid() const { return master && (len >= 0); }
        bool Invalid() const { return !master || len < 0; }
        void Invalidate() { master = 0; len = -1; }
    };
    friend class ScriptVariable::Substring;

    class Iterator : public Substring {
        bool just_started;
    public:
        Iterator(ScriptVariable &master) : Substring(master, 0, 0)
            { just_started = true; }
	bool NextWord(const char *spaces = " \t\n\r");
	bool NextToken(const char *delimiters = ",",
	               const char *trim_spaces = 0);
	bool PrevWord(const char *spaces = " \t\n\r");
	bool PrevToken(const char *delimiters = ",",
	               const char *trim_spaces = 0);
    };
    friend class ScriptVariable::Iterator;

    Substring Range(int pos, int len=-1)
       { return Substring(*this, pos, len); }

    Substring Whole() { return Range(0,-1); }

    Substring Strchr(int c);
    Substring Strrchr(int c);
    Substring Strstr(const char *str);
    Substring Strrstr(const char *str);

    class BadNumber {
        ScriptVariable *var;
    public:
        BadNumber(const ScriptVariable &v);
        BadNumber(const BadNumber &b);
        ~BadNumber();
        const ScriptVariable& Get() { return *var; }
    };

    bool GetLong(long &l) const throw ();
    bool GetDouble(double &d) const throw ();

    long GetLong() const throw (BadNumber);
    double GetDouble() const throw (BadNumber);

    bool GetRational(long &p, long &q, bool throw_bad = false) const
                                                   throw (BadNumber);

private:
    void Unlink();
    void Assign(ScriptVariableImplementation *q);
    void Create(int len);
    void EnsureOwnCopy();
};


#endif
