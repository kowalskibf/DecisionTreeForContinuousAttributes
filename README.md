# Project of "Machine Learning" subject.

Decision Tree that operates both discrete and continuous attributes' values.

Tree can be built using 3 different methods of finding split points for continuous attributes:
- Sorting all rows by the value of one attribute (for each attribute), finding when the output class changes, taking two neighbouring values, for which that happens, computing their average and doing it for every output class change
- Taking min and max of all attribute's values, then splitting values into uniform ranges
- Same as above, but split point, that implies branches with minimum variance, is the only one chosen

Best attributes are found by using Gain and Entropy.

Done in a two-person team.

0 numpy in implementation. Only for analysing result.
