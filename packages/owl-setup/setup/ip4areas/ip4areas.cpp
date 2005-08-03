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




#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "ip4areas.hpp"


IP4IpAddress::IP4IpAddress()
{
  addr = 0xffffffff;
}

IP4IpAddress::IP4IpAddress(const char *a_addr, int preflength)
{
  addr = ntohl(inet_addr(a_addr));
  if(preflength != 32)
     addr &= 0xffffffff << (32 - preflength);
}

IP4IpAddress::IP4IpAddress(unsigned long int hbo_addr)
{
    addr = hbo_addr;
}

IP4IpAddress::IP4IpAddress(const IP4IpAddress &other, int preflength)
{
  addr = other.addr;
  addr &= 0xffffffff << (32 - preflength);
}

IP4IpAddress::IP4IpAddress(const IP4IpAddress &other)
{
  addr = other.addr;
}

IP4IpAddress::~IP4IpAddress()
{
}

bool IP4IpAddress::operator ==(const IP4IpAddress &other) const
{
  return addr == other.addr;
}

IP4IpAddress& IP4IpAddress::operator++()
{
    addr++;
    return *this;
}

IP4IpAddress IP4IpAddress::operator++(int)
{
    IP4IpAddress ret(*this);
    addr++;
    return ret;
}

bool IP4IpAddress::IsInvalid() const
{
  return addr == 0xffffffff;
}

void IP4IpAddress::operator =(const IP4IpAddress &other)
{
  addr = other.addr;
}

bool IP4IpAddress::operator <(const IP4IpAddress &other) const
{
  return addr < other.addr;
}

const char * IP4IpAddress::TextForm() const
{
  static char buf[30];
  sprintf(buf, "%ld.%ld.%ld.%ld",
             addr >> 24 & 0xff,
             addr >> 16 & 0xff,
             addr >>  8 & 0xff,
             addr       & 0xff);
  return buf;
}


IP4Mask::IP4Mask()
{
  len = -1;
}

IP4Mask::IP4Mask(const char* a_mask)
{
  if(a_mask[0] != '/') {
    unsigned long tmp = ntohl(inet_addr(a_mask));
    if(tmp == 0xffffffff && (0!=strcmp(a_mask,"255.255.255.255")))
      len = -1;
    else {
      len = 0;
      while(tmp && (tmp & 1 << 31)) { len++; tmp<<=1; }
      if(tmp) len = -1;
    }
  } else {
    char *endptr;
    long l = strtol(a_mask+1, &endptr, 10);
    if(*endptr != '\0' || *(a_mask+1) == '\0' || l <0 || l>32)
      len = -1;
    else
      len = l;
  }
}

IP4Mask::IP4Mask(int a_len)
{
  if(a_len>=0 && a_len<=32)
    len = a_len;
  else
    len = -1;
}

IP4Mask::IP4Mask(const IP4Mask& other)
{
  len = other.len;
}

IP4Mask::~IP4Mask()
{}

bool IP4Mask::IsInvalid() const
{
  return len == -1;
}

int IP4Mask::Length() const
{
  return len;
}

int IP4Mask::HostCount() const
{
    return 1 << (32 - len);
}

unsigned long IP4Mask::BitMask() const
{
  return len == -1 ? 0xffffffff : (0xffffffff << (32 - len));
}

void IP4Mask::operator =(const IP4Mask &other)
{
  len = other.len;
}

bool IP4Mask::operator ==(const IP4Mask &other) const
{
  return len == other.len;
}

const char * IP4Mask::TextForm() const
{
    static char buf[5];
    sprintf(buf, "/%d", len);
    return buf;
}

const char * IP4Mask::LongTextForm() const
{
    return IP4IpAddress(this->BitMask()).TextForm();
}

IP4Subnet::IP4Subnet()
   : prefix(), mask()
{}

IP4Subnet::IP4Subnet(IP4IpAddress a_addr, IP4Mask a_mask)
   : prefix(a_addr, a_mask.Length()), mask(a_mask)
{}

IP4Subnet::IP4Subnet(const char * a_str)
{
  const char *slashpos = strchr(a_str, '/');
  if(slashpos) {
    mask = IP4Mask(slashpos);
    char *tmp = new char[slashpos-a_str+1];
    memcpy(tmp, a_str, slashpos-a_str);
    tmp[slashpos-a_str]=0;
    prefix = IP4IpAddress(tmp, mask.Length());
  } else {
    prefix = IP4IpAddress(a_str);
    mask = IP4Mask(32);
  }
}

IP4Subnet::~IP4Subnet()
{}

bool IP4Subnet::IsInvalid() const
{
  return prefix.IsInvalid() || mask.IsInvalid();
}

IP4IpAddress IP4Subnet::GetPrefix() const
{
  return prefix;
}

IP4Mask IP4Subnet::GetMask() const
{
  return mask;
}

bool IP4Subnet::operator == (const IP4Subnet &other) const
{
  return mask == other.mask && prefix == other.prefix;
}

bool IP4Subnet::operator <(const IP4Subnet &other) const
{
  return prefix < other.prefix ||
         (prefix == other.prefix && mask.Length() > other.mask.Length());
}

const char * IP4Subnet::TextForm() const
{
  static char buf[40];
  snprintf(buf, sizeof(buf), "%s%s", prefix.TextForm(), mask.TextForm());
  return buf;
}


bool IP4Subnet::IsSubnetOf(const IP4Subnet &other) const
{
  return mask.Length() >= other.mask.Length() &&
            (prefix.HostByteOrderForm() & other.mask.BitMask()) ==
            (other.prefix.HostByteOrderForm() & other.mask.BitMask());
}

bool IP4Subnet::IsSupernetOf(const IP4Subnet &other) const
{
  return mask.Length() <= other.mask.Length() &&
            (prefix.HostByteOrderForm() & mask.BitMask()) ==
            (other.prefix.HostByteOrderForm() & mask.BitMask());
}

bool IP4Subnet::IsComplementary(const IP4Subnet &other) const
{
  IP4Mask shortermask(mask.Length() - 1);
  return (mask.Length() == other.mask.Length()) &&
         (!(prefix == other.prefix)) &&
         ((prefix.HostByteOrderForm() & shortermask.BitMask()) ==
          (other.prefix.HostByteOrderForm() & shortermask.BitMask()));
}

bool IP4Subnet::Contains(IP4IpAddress addr) const
{
    return
        (prefix.HostByteOrderForm() & mask.BitMask()) ==
        (addr.HostByteOrderForm() & mask.BitMask());
}


IP4Subnet IP4Subnet::GetClosestSupernet() const
{
  IP4Mask shortermask(mask.Length() - 1);
  IP4IpAddress shorterprefix(prefix, shortermask.Length());
  return IP4Subnet(shorterprefix, shortermask);
}

IP4Subnet IP4Subnet::GetFirstHalf() const
{
    IP4Mask longermask(mask.Length() + 1);
    unsigned long newpref =
        prefix.HostByteOrderForm() & mask.BitMask();
    return IP4Subnet(IP4IpAddress(newpref), longermask);
}

IP4Subnet IP4Subnet::GetSecondHalf() const
{
    IP4Mask longermask(mask.Length() + 1);
    unsigned long newpref =
        prefix.HostByteOrderForm() | ~ mask.BitMask();
    return IP4Subnet(IP4IpAddress(newpref, longermask.Length()),
                       longermask);
}

IP4IpAddress IP4Subnet::First() const
{
    return IP4IpAddress(prefix.HostByteOrderForm() & mask.BitMask());
}

IP4IpAddress IP4Subnet::Last() const
{
    return IP4IpAddress(prefix.HostByteOrderForm() | ~ mask.BitMask());
}

IP4Area::IP4Area()
{
  first = last = 0;
  text_form_buf = 0;
}

IP4Area::IP4Area(const IP4Area &other)
{
  first = last = 0;
  text_form_buf = 0;
  this->operator+=(other);
}

IP4Area::~IP4Area()
{
  Clean();
  if(text_form_buf) delete[] text_form_buf;
}

bool IP4Area::IsInvalid() const
{
  const ListItem* tmp = first;
  while(tmp) {
      if(tmp->subnet.IsInvalid()) return true;
      tmp = tmp->next;
  }
  return false;
}

int IP4Area::SubnetsCount() const
{
  int i = 0;
  const ListItem* tmp = first;
  while(tmp) {
    i++;
    tmp = tmp->next;
  }
  return i;
}

int IP4Area::HostCount() const
{
  int i = 0;
  const ListItem* tmp = first;
  while(tmp) {
    i += tmp->subnet.HostCount();
    tmp = tmp->next;
  }
  return i;
}

void IP4Area::operator+=(IP4IpAddress ip)
{
    IP4Subnet tmp(ip, 32);
    (*this)+=tmp;
}

void IP4Area::operator-=(IP4IpAddress ip)
{
    IP4Subnet tmp(ip, 32);
    (*this)-=tmp;
}

void IP4Area::operator+=(IP4Subnet op)
{
    ListItem *tmp = AddListItem(op);
    DoAggregationAsPossible(tmp);
}

void IP4Area::operator-=(IP4Subnet op)
{
    ListItem *tmp = first;
    while(tmp) {
        if(tmp->subnet.IsSubnetOf(op)){
            DelListItem(tmp);
            return;
        } else if(tmp->subnet.IsSupernetOf(op)){
            while(tmp->subnet.IsSupernetOf(op) && tmp->subnet != op){
                tmp = SplitListItem(tmp);
                if((tmp->subnet != op) &&
                   !(tmp->subnet.IsSupernetOf(op))) {
                    tmp = tmp->next;
                }
            }
            DelListItem(tmp);
            return;
        }
        tmp = tmp->next;
    }
}

void IP4Area::operator+=(const IP4Area &op)
{
    Iterator iter(op);
    IP4Subnet sub;
    while(iter.GetNext(sub)){
        this->operator+=(sub);
    }
}

void IP4Area::operator-=(const IP4Area &op)
{
    Iterator iter(op);
    IP4Subnet sub;
    while(iter.GetNext(sub)){
        this->operator-=(sub);
    }
}

const IP4Area& IP4Area::operator=(const IP4Area &op)
{
  if(this != &op) {
    Clean();
    this->operator+=(op);
  }
  return *this;
}

void IP4Area::Clean()
{
  while(first) DelListItem(first);
}

bool IP4Area::ReadIn(const char* str)
{
  const char * res = SafeReadIn(str);
  return (*res == 0);
}

const char * IP4Area::SafeReadIn(const char* str)
{
  enum { home, i1, i2, i3, i4, mask, before_comma } state = home;
  const char *p = str;
  const char *first_uneaten_pos = str;
  while(*p) {
    switch(state) {
      case home:
        if(isspace(*p)) {
	  p++;
	  first_uneaten_pos++;
	} else
	if(isdigit(*p)) {
	  state = i1;
	} else goto err;
	break;
      case i1:
        if(isdigit(*p)) {
	  p++;
	} else
	if(*p == '.') {
	  p++; state = i2;
	} else goto err;
	break;
      case i2:
        if(isdigit(*p)) {
	  p++;
	} else
	if(*p == '.') {
	  p++; state = i3;
	} else goto err;
	break;
      case i3:
        if(isdigit(*p)) {
	  p++;
	} else
	if(*p == '.') {
	  p++; state = i4;
	} else goto err;
	break;
      case i4:
        if(isdigit(*p)) {
	  p++;
	} else
	if(*p == '/') {
	  p++; state = mask;
	} else {
	  state = before_comma;
          ReadInSubnet(first_uneaten_pos, p);
	  first_uneaten_pos = p;
	}
	break;
      case mask:
        if(isdigit(*p)) {
	  p++;
	} else {
	  state = before_comma;
          ReadInSubnet(first_uneaten_pos, p);
	  first_uneaten_pos = p;
        }
	break;
      case before_comma:
        if(*p == ',') {
	  p++;
	  state = home;
	  first_uneaten_pos = p;
	} else
	if(isspace(*p)) {
	  p++;
	  first_uneaten_pos++;
	} else goto err;
	break;
    }
  }
  if(state == i4 || state == mask) {
    ReadInSubnet(first_uneaten_pos, p);
    first_uneaten_pos = p;
  }
  err:
  return first_uneaten_pos;
}

void IP4Area::ReadInSubnet(const char *beg, const char *end)
{
  char *buf = new char[end-beg+1];
  memcpy(buf, beg, end-beg);
  buf[end-beg]=0;
  (*this)+=IP4Subnet(buf);
}

const char * IP4Area::TextForm() const
{
  if(!first) return "";
  if(text_form_buf) delete[] text_form_buf;
  const_cast<IP4Area*>(this)->text_form_buf = new char[SubnetsCount()*19];
           // 19 is strlen("000.000.000.000/00,");
  char *p = text_form_buf;
  *p = 0;
  strcpy(p, first->subnet.TextForm());
  while(*p) p++;
  ListItem *tmp = first->next;
  while(tmp) {
    *p=',';
    p++;
    strcpy(p, tmp->subnet.TextForm());
    while(*p) p++;
    tmp = tmp->next;
  }
  return text_form_buf;
}

bool IP4Area::HasAddress(IP4IpAddress addr) const
{
    IP4Subnet tmp(addr, 32);
    return HasSubnet(tmp);
}

bool IP4Area::HasSubnet(const IP4Subnet &subnet) const
{
    ListItem *tmp = first;
    while(tmp) {
        if(tmp->subnet.IsSupernetOf(subnet))
            return true;
        tmp = tmp->next;
    }
    return false;
}

IP4Area::ListItem* IP4Area::AddListItem(const IP4Subnet &a)
{
  ListItem *tmp = new ListItem(a);
  if(!first) {
    first = last = tmp;
  } else {
    ListItem *pos = first;
         // pos will point to the item BEFORE which to insert
    while(pos && pos->subnet < a) {
      pos = pos->next;
    }
    if(!pos) {  // to the end of the list
      tmp->prev = last;
      last->next = tmp;
      last = tmp;
    } else {  // pos->subnet >= a
      tmp->next = pos;
      tmp->prev = pos->prev;
      pos->prev = tmp;
      if(tmp->prev)
        tmp->prev->next = tmp;
      else
        first = tmp;
    }
  }
  return tmp;
}

void IP4Area::DelListItem(const ListItem* p)
{
  if(p->prev)
    p->prev->next = p->next;
  else
    first = p->next;
  if(p->next)
    p->next->prev = p->prev;
  else
    last = p->prev;
  delete p;
}

void IP4Area::DoAggregationAsPossible(const ListItem* p)
{
  if(p->prev && p->subnet.IsSubnetOf(p->prev->subnet)) {
    DelListItem(p);
  } else if(p->next && p->subnet.IsSupernetOf(p->next->subnet)) {
    DelListItem(p->next);
    DoAggregationAsPossible(p);  // It might aggregate with the next subnet
  } else if(p->prev && p->subnet.IsComplementary(p->prev->subnet)) {
    ListItem *tmp = p->prev;
    DelListItem(p);
    tmp->subnet = tmp->subnet.GetClosestSupernet();
    DoAggregationAsPossible(tmp);
  } else if(p->next && p->subnet.IsComplementary(p->next->subnet)) {
    ListItem *tmp = p->next;
    DelListItem(p);
    tmp->subnet = tmp->subnet.GetClosestSupernet();
    DoAggregationAsPossible(tmp);
  }
  // No aggregation was possible, just do nothing
}

IP4Area::ListItem* IP4Area::SplitListItem(ListItem* p)
{
    IP4Subnet s1 = p->subnet.GetFirstHalf();
    IP4Subnet s2 = p->subnet.GetSecondHalf();
    DelListItem(p);
    ListItem *tmp = AddListItem(s1);
    AddListItem(s2);
    return tmp;
}


IP4Area::Iterator::Iterator(const IP4Area &area)
{
  current = area.first;
}

IP4Area::Iterator::~Iterator()
{}

bool IP4Area::Iterator::GetNext(IP4Subnet &net)
{
  if(current) {
    net = current->subnet;
    current = current->next;
    return true;
  } else {
    return false;
  }
}

IP4Area::HostIterator::HostIterator(const IP4Area &area)
{
    current = area.first;
    if(current)
        curip = current->subnet.GetPrefix();
}

IP4Area::HostIterator::~HostIterator()
{}

bool IP4Area::HostIterator::GetNext(IP4IpAddress &addr)
{
    if(!current)
        return false;
    addr = curip;
    curip++;
    if(!current->subnet.Contains(curip)) {
        current = current->next;
        if(current)
            curip = current->subnet.GetPrefix();
    }
    return true;
}


