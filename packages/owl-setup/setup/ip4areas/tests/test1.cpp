// +-------------------------------------------------------------------------+
// |                     IP4areas library vers. 0.3.1                        |
// | Copyright (c) Andrey Vikt. Stolyarov <crocodil_AT_croco.net>  2002-2006 |
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




#include <string>
#include "ip4areas.hpp"
#include "tests.hpp"

using namespace std;

int main ()  {
    TESTS_SECTION_BEGIN;
    TESTING_CLASS("IP4IpAddress");
    {
        IP4IpAddress *a1, *a2, *a3, *a4, *a5, *a6;
        a1 = new IP4IpAddress("1.2.3.4");
        a2 = new IP4IpAddress("2.3.4.5");
        a3 = new IP4IpAddress("1.2.3.4");
        a4 = new IP4IpAddress("invalid_address");
        a5 = new IP4IpAddress("666.777.888.999");
        a6 = new IP4IpAddress("255.255.255.255");
        TEST_TRUE("equality", (*a1 == *a3));
        TEST_TRUE("non-equality", (!(*a1 == *a2)));
        TEST_TRUE("valid1", ! a1->IsInvalid());
        TEST_TRUE("valid2", ! a2->IsInvalid()); 
        TEST_TRUE("valid3", ! a3->IsInvalid()); 
        TEST_TRUE("invalid1", a4->IsInvalid()); 
#ifndef __sun__
        TEST_TRUE("invalid2", a5->IsInvalid()); 
#endif
        TEST_TRUE("invalid3", a6->IsInvalid()); 
        TEST_TRUE("textform", a1->TextForm() == string("1.2.3.4"));
        TEST_TRUE("less", *a1 < *a2);
        TEST_TRUE("no-less", !(*a2 < *a1));
        TEST_TRUE("eq-no-less", !(*a1 < *a3));
        delete a6;
        delete a5;
        delete a4;
        delete a3;
        delete a2;
        delete a1;
    }
    TESTING_CLASS("IP4Mask");
    { 
        IP4Mask m1("255.255.255.240");
        IP4Mask m2("/27");
        IP4Mask m3(26);
        IP4Mask m4("255.255.255.255");
        IP4Mask m5("265.2.2.2");
        IP4Mask m6("invalid_mask");
        IP4Mask m7("255.254.255.240");
        TEST_TRUE("by_qdn", m1.Length() == 28);
        TEST_TRUE("by_suffix", m2.Length() == 27);
        TEST_TRUE("by_lenght", m3.Length() == 26);
        TEST_TRUE("valid1", ! m4.IsInvalid());
        TEST_TRUE("valid2", ! m1.IsInvalid());
        TEST_TRUE("invalid1", m5.IsInvalid());
        TEST_TRUE("invalid2", m6.IsInvalid());
        TEST_TRUE("invalid3", m7.IsInvalid());
        TEST_TRUE("extract", m1.BitMask() == 0xfffffff0);
        TEST_TRUE("textform", m2.TextForm() == string("/27"));
        TEST_INTEGER("hostcount1", m1.HostCount(), 16);
        TEST_INTEGER("hostcount2", m2.HostCount(), 32);
        TEST_INTEGER("hostcount3", m3.HostCount(), 64);
        TEST_INTEGER("hostcount4", m4.HostCount(), 1);

        TEST_STRING("long_text_form", m2.LongTextForm(), "255.255.255.224");
    }
    TESTING_CLASS("IP4Subnet");
    {
        IP4Subnet s1("194.87.251.18/24");
        IP4Subnet s2("194.87.251.18/32");
        IP4Subnet s3("194.87.251.18/32");
        IP4Subnet s4(IP4IpAddress("194.87.251.18"), IP4Mask(24));
        IP4Subnet s5("195.42.160.10/24");
        IP4Subnet s6("194.87.251.25/24");
        IP4Subnet s7("194.87.251.25/28");
        IP4Subnet s8("195.42.160.16/28");
        IP4Subnet s9("195.42.160.0/28");
        IP4Subnet s10("195.42.160.32/28");
        IP4Subnet s11("195.42.160.8/29");
        IP4Subnet s12("195.42.160.0/29");

        IP4Subnet s13("195.42.160.1"); // valid
        IP4Subnet s14("195.42.160.1/33"); // invalid
        IP4Subnet s15("195,42.160.1/33"); // invalid
        
        TEST_TRUE("addr/24", s1.GetPrefix() == IP4IpAddress("194.87.251.0"));
        TEST_TRUE("mask/24", s1.GetMask() == IP4Mask(24));
        TEST_INTEGER("subnet_hostcount", s1.HostCount(), 256);
        TEST_TRUE("equality", s1 == s4);
        TEST_TRUE("equality2", s2 == s3);
        TEST_TRUE("equality3", s1 == s6);
        TEST_TRUE("non-equality", ! (s1 == s3));
        TEST_TRUE("non-equality2", ! (s1 == s3));
        TEST_STRING("textform", s2.TextForm(), string("194.87.251.18/32"));
        TEST_STRING("textform2", s3.TextForm(), string("194.87.251.18/32"));
        TEST_STRING("textform2", s7.TextForm(), string("194.87.251.16/28"));
        TEST_TRUE("supernet", s5.IsSupernetOf(s8));
        TEST_TRUE("subnet", s8.IsSubnetOf(s5));
        TEST_TRUE("no-supernet", !s5.IsSupernetOf(s7));
        TEST_TRUE("no-subnet", !s5.IsSubnetOf(s8));
        TEST_TRUE("complementary", s8.IsComplementary(s9));
        TEST_TRUE("complementary2", s9.IsComplementary(s8));
        TEST_TRUE("non-complementary", !s8.IsComplementary(s10));
        TEST_TRUE("non-complementary2", !s8.IsComplementary(s11));
        TEST_TRUE("get-closest-supernet",
                  s11.GetClosestSupernet() == s9);
        TEST_TRUE("get-first-half", s9.GetFirstHalf() == s12);
        TEST_TRUE("get-second-half", s9.GetSecondHalf() == s11);

        TEST_TRUE("subnet_as_addr_valid", !s13.IsInvalid());
        TEST_TRUE("subnet_invalid2", s14.IsInvalid());
        TEST_TRUE("subnet_invalid3", s15.IsInvalid());

        IP4Subnet s16("192.168.5.19/28");
        TEST_STRING("subnet_first", s16.First().TextForm(), "192.168.5.16");
        TEST_STRING("subnet_last", s16.Last().TextForm(), "192.168.5.31");
    }
    TESTING_CLASS("IP4Area");
    {
        IP4Area a1;
        TEST_TRUE("empty", a1.SubnetsCount() == 0);
        
        IP4Area a2;
        a2 += IP4Subnet("10.0.1.16/29");
        a2 += IP4Subnet("10.2.0.24/29");
        TEST_INTEGER("adding", a2.SubnetsCount(), 2);
        
        IP4Area a3;
        a3 += IP4Subnet("10.0.0.16/29");
        a3 += IP4Subnet("10.0.0.24/29");
        TEST_TRUE("complementary", a3.SubnetsCount() == 1);
        
        IP4Area a4;
        a4 += IP4Subnet("10.0.2.0/24");
        a4 += IP4Subnet("10.0.3.128/25");  // 128 - 255
        a4 += IP4Subnet("10.0.3.0/26");    // 0 - 63
        a4 += IP4Subnet("10.0.3.64/28");   // 64 - 79
        a4 += IP4Subnet("10.0.3.96/27");   // 96 - 127
        TEST_TRUE("non-aggregatable", a4.SubnetsCount() == 5);
        TEST_STRING("proper-order", a4.TextForm(), string(
            "10.0.2.0/24,10.0.3.0/26,10.0.3.64/28,10.0.3.96/27,10.0.3.128/25"))
            a4 += IP4Subnet("10.0.3.80/28");   // 80 - 95
        TEST_INTEGER("huge_aggregation", a4.SubnetsCount(), 1);
        if(TESTS_lasttestfailed)
            printf("%s\n", a4.TextForm());
        
        IP4Area a5;
        a5.ReadIn("   10.0.0.0/24, 10.1.1.0/25,10.2.2.2/32");
        TEST_STRING("read-in",a5.TextForm(),"10.0.0.0/24,10.1.1.0/25,10.2.2.2/32");
        IP4Area::Iterator iter(a5);
        IP4Subnet s1;
        iter.GetNext(s1);
        TEST_TRUE("iteration1", s1 == IP4Subnet("10.0.0.0/24"));
        iter.GetNext(s1);
        TEST_TRUE("iteration2", s1 == IP4Subnet("10.1.1.0/25"));
        iter.GetNext(s1);
        TEST_TRUE("iteration3", s1 == IP4Subnet("10.2.2.2/32"));
        TEST_TRUE("iteration_end", !(iter.GetNext(s1)));
        TEST_TRUE("has_address", a5.HasAddress(IP4IpAddress("10.0.0.90")));
        TEST_TRUE("hasnt_address", !a5.HasAddress(IP4IpAddress("10.100.0.90")));
        TEST_TRUE("has_subnet", a5.HasSubnet(IP4Subnet("10.0.0.16/28")));
        TEST_TRUE("has_subnet2", a5.HasSubnet(IP4Subnet("10.1.1.0/25")));
        TEST_TRUE("has_subnet3", a5.HasSubnet(IP4Subnet("10.2.2.2/32")));
        TEST_TRUE("hasnt_subnet", !a5.HasSubnet(IP4Subnet("10.0.0.0/20")));
        TEST_TRUE("hasnt_subnet2", !a5.HasSubnet(IP4Subnet("10.2.2.2/31")));
        TEST_TRUE("hasnt_subnet3", !a5.HasSubnet(IP4Subnet("10.1.1.0/24")));

        IP4Area a6;
        a6.ReadIn("10.3.3.0/24, 10.0.0.0/16,10.2.2.0/24");
        a6 -= IP4Subnet("10.2.2.0/24");
        TEST_INTEGER("remove_exact_net", a6.SubnetsCount(), 2);
        a6 -= IP4Subnet("10.3.0.0/20");
        TEST_INTEGER("remove_supernet", a6.SubnetsCount(), 1);
        a6 -= IP4Subnet("10.0.17.0/24");
        TEST_INTEGER("remove_sub_subnet", a6.SubnetsCount(), 8);
        if(TESTS_lasttestfailed)
            printf("%s\n", a6.TextForm());

        IP4Area a7;
        a7.ReadIn("10.10.10.0/29");
        a7 -= IP4Subnet("10.10.10.4/30");
        TEST_STRING("remove_second_half", a7.TextForm(),
                    "10.10.10.0/30");
        a7 -= IP4Subnet("10.10.10.0/31");
        TEST_STRING("remove_first_half", a7.TextForm(),
                    "10.10.10.2/31");

        IP4Area a8, a9;
        a8.ReadIn("10.0.0.0/16");
        a9.ReadIn("10.0.1.0/24, 10.0.128.0/18");
        a8 -= a9;
        TEST_INTEGER("remove_area_from_area", a8.SubnetsCount(), 8);
        if(TESTS_lasttestfailed)
            printf("%s\n", a8.TextForm());

        IP4Area a10, a11;
        a10.ReadIn("10.0.10.0/24, 10.0.20.0/22");
        a11.ReadIn("10.0.128.0/17, 10.0.22.0/24");
        a10 += a11;
        TEST_INTEGER("add_area_to_area", a10.SubnetsCount(), 3);
        if(TESTS_lasttestfailed)
            printf("%s\n", a8.TextForm());


        IP4Area a20;
        bool good = a20.ReadIn("some shit");
        TEST_TRUE("area_invalid", !good);
//        IP4Area a21;
//        a21.ReadIn("195.42.150.10/10, 195.7 20.25/10");
//        TEST_TRUE("area_invalid2", a21.IsInvalid());
//        IP4Area a22;
//        a22.ReadIn("10.20.30.40");
//        TEST_TRUE("area_invalid", a22.IsInvalid());

        
        IP4Area a30;
        a30.ReadIn("10.0.0.0/31, 10.12.14.16, 11.11.11.11");
        TEST_INTEGER("hostcount", a30.HostCount(), 4);
        IP4Area::HostIterator iter30(a30);
        IP4IpAddress ip30;
        iter30.GetNext(ip30);
        TEST_TRUE("hostiteration1", ip30 == IP4IpAddress("10.0.0.0"));
        iter30.GetNext(ip30);
        TEST_TRUE("hostiteration2", ip30 == IP4IpAddress("10.0.0.1"));
        iter30.GetNext(ip30);
        TEST_TRUE("hostiteration3", ip30 == IP4IpAddress("10.12.14.16"));
        iter30.GetNext(ip30);
        TEST_TRUE("hostiteration4", ip30 == IP4IpAddress("11.11.11.11"));
        TEST_TRUE("hostiteration_end", !(iter30.GetNext(ip30)));
        
        
    }
    TESTS_SECTION_END
    return 0;
}
