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




CXX = g++
CXXFLAGS = -Wall -g

FILES = ip4areas.o

libip4areas.a: $(FILES)	
	$(AR) -crs $@ $(FILES)

%.o:	%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@


run:
	cd tests && $(MAKE) run

clean:
	rm -f *.o *~ buf libip4areas.a
	cd tests && $(MAKE) clean
