CXXFLAGS = -O2 -Wall -lm

c11:
	gcc -o ../$(FILE) ../$(FILE).c $(CXXFLAGS) -std=gnu11
c99:
	gcc -o ../$(FILE) ../$(FILE).c $(CXXFLAGS) -std=gnu99
cpp:
	g++ -o ../$(FILE) ../$(FILE).cpp $(CXXFLAGS) -std=gnu++17
c-fsan:
	gcc -o ../$(FILE) ../$(FILE).c $(CXXFLAGS) -std=gnu99 -fsanitize=address -g
cpp-fsan:
	g++ -o ../$(FILE) ../$(FILE).cpp $(CXXFLAGS) -std=gnu++17 -fsanitize=address -g
java:
	javac -J-Xms1024m -J-Xmx1920m -J-Xss512m -encoding UTF-8 ../$(FILE).java
python:
	echo "Python"
clean:
	rm -f ../$(FILE)
	rm -f ../$(FILE).class