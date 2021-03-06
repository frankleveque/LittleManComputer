LittleManComputer
====

This project implements a Little Man Computer simulation
https://en.wikipedia.org/wiki/Little_man_computer

Note: Mailboxes can hold values greater than 3 digits. The script that squares
numbers up to 999 now works without overflow. 

---

`lmc_simulator.cpp` the simulator in c++

`lmc_compiler.py` "compiles" LMC assembly to the format the simulator takes

`unit_tests.py` unit tests

`example_scripts` contains some scripts you can compile

--- 

The compiler can compile any number of scripts at once.

The simulator will only run one file at a time, ignoring the rest.


Make the simulator with:

``` g++ -std=c++11 lmc_simulator.cpp -o lmc_simulator.exe ```

"Compile" lmc scripts with:

``` python3 lmc_compiler.py <script file(s).lm> ``` 


Then run *.compiled scripts with 

``` ./lmc_simulator.exe <filename.compiled> ```








