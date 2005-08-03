// +-------------------------------------------------------------------------+
// |                     IP4areas library vers. 0.3.0                        |
// | Copyright (c) Andrey Vikt. Stolyarov <crocodil_AT_croco.net>  2002-2005 |
// | ----------------------------------------------------------------------- |
// | This is free software.  Permission is granted to everyone to use, copy  |
// |        or modify this software under the terms and conditions of        |
// |                 GNU LESSER GENERAL PUBLIC LICENSE, v. 2.1               |
// |     as published by Free Software Foundation (see the file LGPL.txt)    |
// |                                                                         |
// | Please visit http://www.croco.net/software/ip4areas to get a fresh copy |
// | ----------------------------------------------------------------------- |
// |   This code is provided strictly and exclusively on the "AS IS" basis.  |
// | !!! THERE IS NO WARRANTY OF ANY KIND, NEITHER EXPRESSED NOR IMPLIED !!! |
// +-------------------------------------------------------------------------+




#ifndef IPARYTHM_HPP_SENTRY
#define IPARYTHM_HPP_SENTRY


class IP4IpAddress {
    unsigned long addr; //!< The address is stored in the host byte order
public:
    IP4IpAddress(); /* creates invalid ip address (0xf...f) */
    IP4IpAddress(const char* a_addr, int preflength = 32);
    IP4IpAddress(unsigned long hostorderformaddr);
    IP4IpAddress(const IP4IpAddress &other, int preflength);
    IP4IpAddress(const IP4IpAddress &other);
    ~IP4IpAddress();

    bool operator ==(const IP4IpAddress &other) const;
    bool operator <(const IP4IpAddress &other) const;
    IP4IpAddress& operator++();
    IP4IpAddress  operator++(int);

    bool IsInvalid() const;

    void operator =(const IP4IpAddress &other);

    const char* TextForm() const;
    unsigned long HostByteOrderForm() const { return addr; }
};

class IP4Mask {
    char len;
public:
    IP4Mask();
    IP4Mask(const char* a_mask);
    IP4Mask(int a_len);
    IP4Mask(const IP4Mask &other);
    ~IP4Mask();

    bool IsInvalid() const;
    int Length() const;
    unsigned long BitMask() const;
    int HostCount() const;

    bool operator ==(const IP4Mask &other) const;
    void operator =(const IP4Mask &other);

    const char * TextForm() const;      /* "/24" */
    const char * LongTextForm() const;  /* "255.255.255.0" */
};


class IP4Subnet {
    IP4IpAddress prefix;
    IP4Mask mask;
public:
    IP4Subnet();
    IP4Subnet(IP4IpAddress a_addr, IP4Mask a_mask);
    IP4Subnet(const char *a_str);
    ~IP4Subnet();

    bool IsInvalid() const;

    IP4IpAddress GetPrefix() const;
    IP4Mask GetMask() const;
    int HostCount() const { return GetMask().HostCount(); }

    bool operator==(const IP4Subnet &other) const;
    bool operator <(const IP4Subnet &other) const;
    bool operator!=(const IP4Subnet &other) const
        { return !(other==*this); }

    bool IsSubnetOf(const IP4Subnet &other) const;
    bool IsSupernetOf(const IP4Subnet &other) const;
    bool IsComplementary(const IP4Subnet &other) const;
    bool Contains(IP4IpAddress) const;

    IP4Subnet GetClosestSupernet() const;
    IP4Subnet GetFirstHalf() const;
    IP4Subnet GetSecondHalf() const;

    IP4IpAddress First() const;
    IP4IpAddress Last() const;

    const char * TextForm() const;
};

class IP4Area {
    struct ListItem {
        ListItem *prev;
        ListItem *next;
        IP4Subnet subnet;
        ListItem() : subnet() { prev = next = 0; }
        ListItem(const IP4Subnet &a) : subnet(a) { prev = next = 0; }
    };
    ListItem *first, *last;

    char *text_form_buf;
public:
    IP4Area();
    IP4Area(const IP4Area &other);
    ~IP4Area();

    bool IsInvalid() const;

    int SubnetsCount() const;
    int HostCount() const;

    void operator+=(IP4IpAddress ip);
    void operator-=(IP4IpAddress ip);
    void operator+=(IP4Subnet subnet);
    void operator-=(IP4Subnet subnet);
    void operator+=(const IP4Area &area);
    void operator-=(const IP4Area &area);

    const IP4Area& operator =(const IP4Area &other);

    void Clean();

    bool ReadIn(const char* areadescr);
    const char * SafeReadIn(const char* areadescr);
    const char * TextForm() const;

    bool HasAddress(IP4IpAddress addr) const;
    bool HasSubnet(const IP4Subnet &subnet) const;

    class Iterator {
        const ListItem *current;
    public:
        Iterator(const IP4Area &area);
        ~Iterator();
        bool GetNext(IP4Subnet &net);
    };
    friend class IP4Area::Iterator;

    class HostIterator {
        const ListItem *current;
        IP4IpAddress curip;
    public:
        HostIterator(const IP4Area &area);
        ~HostIterator();
        bool GetNext(IP4IpAddress &addr);
    };
    friend class IP4Area::HostIterator;

private:
    ListItem* AddListItem(const IP4Subnet &a);
    void DelListItem(const ListItem *item);
    void DoAggregationAsPossible(const ListItem *item);
    ListItem* SplitListItem(ListItem *item);
    void ReadInSubnet(const char *beg, const char *end);
};



#endif
