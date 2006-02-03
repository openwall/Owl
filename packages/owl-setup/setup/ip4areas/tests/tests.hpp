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




#ifndef TESTS_HPP_SENTRY
#define TESTS_HPP_SENTRY

#include <stdio.h>
#include <stdlib.h>
#define TESTS_SECTION_BEGIN \
  int TESTSCount = 0; \
  int TESTSPassed = 0; \
  int TESTSFailed = 0; \
  int TESTS_lasttestfailed;

#define TESTS_SECTION_END \
  printf("@@@ ---------------------\n");\
  printf("@@@ - Passed:\t%d\n", TESTSPassed);\
  printf("@@@ - Failed:\t%d\n", TESTSFailed);\
  printf("@@@ - Totals:\t%d\n", TESTSCount);

#define TESTS_MESSAGE(msg) \
  printf("@@@ <*> %s\n", (msg).c_str());

#define TESTING_CLASS(name) \
  printf("@@@ --- %s --- \n", string(name).c_str());

#define TEST_TRUE(name, condition) \
  TESTSCount++; \
  if((condition)) { \
     TESTS_MESSAGE(string("passed ") + (name))\
     TESTSPassed++;\
     TESTS_lasttestfailed = false;\
  }else{\
     TESTS_MESSAGE(string("FAILED ") + (name))\
     TESTSFailed++;\
     TESTS_lasttestfailed = true;\
  }

#define TEST_STRING(name, value, expected_val) {\
    TESTSCount++; \
    string TESTSlocalval = value;\
    if(TESTSlocalval == expected_val) { \
       TESTS_MESSAGE(string("passed ") + (name))\
       TESTSPassed++;\
       TESTS_lasttestfailed = false;\
    }else{\
       TESTS_MESSAGE(string("FAILED ") + (name) + \
                     " value:[" + TESTSlocalval + "], expected:[" + \
                     expected_val + "]")\
       TESTSFailed++;\
       TESTS_lasttestfailed = true;\
    }\
  }

#define TEST_INTEGER(name, value, expected_val) \
  TESTSCount++; \
  { int TESTSlocalval = value;\
    if(TESTSlocalval == expected_val) { \
       TESTS_MESSAGE(string("passed ") + (name))\
       TESTSPassed++;\
       TESTS_lasttestfailed = false;\
    }else{\
       char TESTSbuf[250]; \
       sprintf(TESTSbuf, "FAILED %s value:[%d] expected:[%d]",\
                     (name), TESTSlocalval, expected_val);\
       TESTS_MESSAGE(string(TESTSbuf))\
       TESTSFailed++;\
       TESTS_lasttestfailed = true;\
    }\
  }






#endif
