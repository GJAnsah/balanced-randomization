# Balanced Randomization

Randomization methods that maintain balance across choices — for experimental designs, staircase procedures, and adaptive trials.



#### Use-Cases

* ###### BalancedRand

&nbsp;	Draws random option from a list of options with a constraint that difference in draw counts between the least draw and most drawn option is less than a fixed threshold - max\_imbalance.



* ###### SoftBalancedRand

 	Draws random option from a list of options with a constraint that difference in draw counts between the least draw and most drawn option is less than a variable threshold - \[1,max\_imbalance].





| Method | Balance | Predictability | Use when |

|--------|---------|----------------|----------|

| BalancedRand | Tight | Higher at threshold | Balance matters most |

| SoftBalancedRand | Slightly looser | Lower | Unpredictability matters |

#### Installation

git clone 'https://github.com/GJAnsah/balanced-randomization.git'





#### Usage

```python



from balanced\_randomization import BalancedRand, SoftBalancedRand





num\_trials = 100

num\_choices=2

max\_imbalance=3



balanced = BalancedRand(num\_choices,max\_imbalance)

softbalanced = SoftBalancedRand(num\_choices,max\_imbalance)



\#draw balanced random numbers



for \_ in range(num\_trials):

&nbsp;	balanced.draw()

&nbsp;	softbalanced.draw()





\#display

print(balanced.get\_counts())

print(softbalanced.get\_counts())

```



##### Testing



Run the test file to compare methods:

```bash

cd balanced-randomization

python tests/test\_methods.py

```



Or customize parameters:

```python

from tests.test\_methods import run\_tests



run\_tests(num\_trials=50, num\_choices=2, num\_experiments=500,block\_size=4, max\_imbalance=3)

```



###### Sample Results

|Method    |             Mean Imb  |   Max Imb   |   Predictability|

|-----------|-----------------------|-------------|-----------------------|

|Pure Random           | 4.10        | 14.14       | 46.0 %|

|Block Random          | 0.49        | 1.41        | 74.0 %|

|Balanced Random       | 0.96        | 1.41        | 54.0 %|

|Soft Balanced Random  | 0.51        | 1.41        | 52.0 %|



###### License

MIT



