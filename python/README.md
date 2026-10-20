# Theatrical Players Refactoring Kata - Python version

## Part 1 – Understand the Existing Code

1. Clone the repository, select one of the permitted languages, and examine the starter code.
   I used Python for the code.

2. Identify at least three aspects of the existing implementation that make it difficult to understand,
   maintain, or extend.
   a. The statement function is a very long function that already hints a need of refactoring. Long functions are typically not good especially when handling multiple processes such as calculating prices, credits, and formmatting the output text. This makes it hard to fix bugs when certain parts of the program fails and makes it so that you have to consider the whole scope of the program to identify what is actually causing an error. This makes testing also very memory intensive because you have to call the whole function in order to test certain parts of the algorithm.
   b. The numbers are also not explicitly said to be in a certain conversion. Just initially looking at it, the number 40000 seems like it would be 40,000 but after examining the example test statement, I realized that it's actually $400.00. So a simple comment that specifies the number's value or a decimal conversion of all of the numbers would be beneficial in helping me understand what the numbers mean.
   c. It seems like data are being passed using dictionaries. This is risky because lookups like invoice['performances'] or perf['audience'] are string kets with no type checking. So, a simple typo for the string key would cause a lot of confusions when the code runs.

3. Before modifying the implementation, run the supplied automated tests and record the results
   (including how to run the tests).
   First, cd into the project directory in the terminal (if not already done). Then, you need to create a virtual environment in order to test the code using pytest. To do that, you need to use this command to create the environment:
   python3 -m venv .venv #you can use either python or python3
   After that, you need to activate the virtual env:
   source .venv/bin/activate
   Then, install all of the dependencies:
   pip install -r requirements.txt
   And now, you can run test_statement.py using pytest:
   python -m pytest -v

After that, the results should show the following:
collected 2 items

tests/test_statement.py::test_example_statement PASSED [ 50%]
tests/test_statement.py::test_statement_with_new_play_types PASSED [100%]

==================================== 2 passed in 0.02s =====================================

## Part 2 – Refactor the code

Refactoring 1: Simplifying the statment function by dividing it into smalle rfunctions
(a) I moved the tragedy/comedy charge calculation out of the loop into its own function, amount_for(performance), and the volume-credit logic into volume_credits_for(performance). I replaced the play variable with a play_for(performance) function. I renamed format_as_dollars to usd, and it now divides by 100 itself.

(b) The original statement function was one long block doing several jobs. Each new function has a clear name and does one thing, so the loop is easier to read. Removing temporary variables also made the next steps easier.

(c) I ran pytest -q and both supplied tests passed. The approval test compares the whole statement text against the approved file, so any change to amounts, credits or formatting would have failed.

Refactoring 2: Dividing the loop into separate calculations
(a) The loop used to add up the total amount, add up the volume credits and build the output all at once. I removed the running totals and replaced them with total_amount() and total_volume_credits(), which each use sum(). The loop now only builds the output lines and doesn't have to worry about calculations.

(b) Each piece of code now has one job. The totals no longer depend on how far the loop has run, so they can be calculated on their own.

(c) I ran pytest -q and both tests passed. The approved file's totals ($1,730.00 and 47 credits) still matched.

Refactoring 3: Separating the calculations from formatting the text ouputs
(a) I created create_statement_data.py. Its create_statement_data(invoice, plays) function builds a list of performance data (play, audience, amount, volume credits) and returns it with the customer name and both totals. statement() now just calls render_plain_text(create_statement_data(invoice, plays)), and render_plain_text only formats the text.

(b) Calculating charges and printing the statement are separate concerns. Now the pricing rules can change without touching the formatting, and a new output format such as HTML could reuse the same data without copying any calculations.

(c) I ran pytest -q and both tests passed. The approval test showed the printed text was unchanged, and the unknown-type test showed a ValueError is still raised.

Refactoring 4: Replacing if/else statements with polymorphism techniques
(a) I replaced the if/elif on play type with classes. PerformanceCalculator is a base class with the shared volume-credit rule. TragedyCalculator and ComedyCalculator each have their own amount(), and ComedyCalculator adds the extra comedy credits in volume_credits(). create_performance_calculator returns the right class for the play type, or raises ValueError for an unknown type.

(b) Each play type's rules are now kept in one class, and the rest of the code doesn't need to check the type. Adding a new play type means adding one new class and one check in create_performance_calculator, without changing the existing classes. That's what makes Part 4 (historical plays) easy.

(c) I ran pytest -q and both tests passed. The approval test covers tragedy and comedy pricing and credits. The new-play-types test confirms that "history" and "pastoral" still raise ValueError.

## Part 3 – Improve the Automated Tests

I implemented the following two tests and they both passed for both the original code and the current one:
Test 1: test_tragedy_audience_boundary_at_30
Tragedy performances charge extra and give volume credits only for audience members over 30. This test checks if the number of audiences is exactly 30 ($400.00, 0 credits) and 31 ($410.00, 1 credit). It makes sure nothing extra is charged or credited at 30, and that the extra starts at 31.

Test 2: test_comedy_audience_boundary_at_20
Comedy performances add a $100 surcharge plus $5 per person once the number of audiences is over 20, and give 1 bonus credit per 5 people. This test checks if an audience of exactly 20 people ($360.00) and 21 ($468.00), with 8 credits in total. It would catch an off-by-one mistake such as >= 20 instead of > 20, and it also checks the comedy bonus credit rule.

## Part 4 – Extend the Application

Part 4 – Extend the Application
After finishing the refactoring, I added support for a new play type called "historical". The rules are:
- Base charge of $500.
- For an audience larger than 20, add $15 per person beyond 20.
- 1 volume credit for every 5 audience members (rounded down).

How I added it:
Because of the polymorphism refactoring in Part 2, adding a new play type only needed two changes in create_statement_data.py:
1. A new HistoricalCalculator class (a subclass of PerformanceCalculator) with its own amount() and volume_credits().
2. One new check in create_performance_calculator that returns a HistoricalCalculator when the play type is "historical".
I did not need to change TragedyCalculator, ComedyCalculator, statement.py, or the formatting code at all, so the original play types keep their behavior.

One design decision: HistoricalCalculator overrides volume_credits() completely instead of adding to the base class rule. The base rule gives 1 credit for each audience member over 30, but the historical rules only give 1 credit per 5 people. The example in the assignment confirms this: an audience of 35 should earn 7 credits (35 / 5). If historical plays also got the base credits, it would be 5 + 7 = 12 credits.

Tests for historical plays (in tests/test_historical.py):
- test_historical_example_from_spec: checks the example from the assignment. An audience of 35 is charged $725.00 ($500 + 15 x $15) and earns 7 credits.
- test_historical_audience_boundary_at_20: boundary test with an audience of exactly 20 and 21. At 20, the charge is just the $500.00 base. At 21, $15 is added for $515.00. Both earn 4 credits, for 8 total.
- test_historical_with_original_play_types: puts a tragedy, a comedy, and a historical play on the same invoice. This checks that the original play types are still charged the same as before ($650.00 for Hamlet and $580.00 for As You Like It, same as the original approved output) when a historical play is added.

The supplied test_statement_with_new_play_types still passes, since its plays use the types "history" and "pastoral", which are still unknown and still raise a ValueError.

Final test results:
python -m pytest -v

tests/test_historical.py::test_historical_example_from_spec PASSED        [ 14%]
tests/test_historical.py::test_historical_audience_boundary_at_20 PASSED  [ 28%]
tests/test_historical.py::test_historical_with_original_play_types PASSED [ 42%]
tests/test_statement.py::test_example_statement PASSED                    [ 57%]
tests/test_statement.py::test_statement_with_new_play_types PASSED        [ 71%]
tests/test_statement.py::test_tragedy_audience_boundary_at_30 PASSED      [ 85%]
tests/test_statement.py::test_comedy_audience_boundary_at_20 PASSED       [100%]

7 passed
