# +-------------------------------------------------------------------------+
# |                     IP4areas library vers. 0.3.0                        |
# | Copyright (c) Andrey Vikt. Stolyarov <crocodil_AT_croco.net>  2002-2005 |
# | ----------------------------------------------------------------------- |
# | This is free software.  Permission is granted to everyone to use, copy  |
# |        or modify this software under the terms and conditions of        |
# |                 GNU LESSER GENERAL PUBLIC LICENSE, v. 2.1               |
# |     as published by Free Software Foundation (see the file LGPL.txt)    |
# |                                                                         |
# | Please visit http://www.croco.net/software/ip4areas to get a fresh copy |
# | ----------------------------------------------------------------------- |
# |   This code is provided strictly and exclusively on the "AS IS" basis.  |
# | !!! THERE IS NO WARRANTY OF ANY KIND, NEITHER EXPRESSED NOR IMPLIED !!! |
# +-------------------------------------------------------------------------+





TESTS = test1
CPPFLAGS = -I..
CXXFLAGS = -ggdb -Wall -O0

archstring := $(shell uname)
ifneq (,$(findstring SunOS, $(archstring)))
LDFLAGS=-lsocket -lnsl
else
LDFLAGS=
endif



%.o:	%.cpp tests.hpp ../ip4areas.hpp
	$(CXX) -c $< $(CXXFLAGS) $(CPPFLAGS)


test1:	test1.o ../libip4areas.a
	$(CXX) $^ $(CXXFLAGS) -o $@ $(LDFLAGS)

../libip4areas.a: FORCE
	cd .. && $(MAKE)

run:	$(TESTS)
	for T in $(TESTS) ; do \
	  ./$$T ;  \
	done

clean:
	rm -f *.o $(TESTS)


FORCE:
