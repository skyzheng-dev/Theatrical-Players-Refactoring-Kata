# Theatrical Players Refactoring Kata - Python version

## Part 1 – Understand the Existing Code

1. Clone the repository, select one of the permitted languages, and examine the starter code.
   I used Python for the code.

2. Identify at least three aspects of the existing implementation that make it difficult to understand,
   maintain, or extend.
   a. The statement function is a very long function that already hints a need of refactoring. Long functions are typically not good especially when handling multiple processes such as calculating prices, credits, and formmatting the output text. This makes it hard to fix bugs when certain parts of the program fails and makes it so that you have to consider the whole scope of the program to identify what is actually causing an error. This makes testing also very convoluted because you have to call the whole function in order to test certain parts of the algorithm.
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
Comedy performances add a $100 surcharge plus $5 per person once the number of audiences is over 20, and give 1 bonus credit per 5 people. This test checks for an audience of exactly 20 people ($360.00) and 21 people ($468.00), with 8 credits in total. It would catch an off-by-one mistake such as >= 20 instead of > 20, and it also checks the comedy bonus credit rule.

## Part 4 – Extend the Application

What I did:

1. A new HistoricalCalculator class (a subclass of PerformanceCalculator) with its own amount() and volume_credits().
2. One new check in create_performance_calculator that returns a HistoricalCalculator when the play type is "historical". I did not need to change TragedyCalculator, ComedyCalculator, statement.py, or the formatting code at all, so the original play types keep their behavior. HistoricalCalculator basically replaces volume_credits() completely instead of building on the original class rule, because historical plays don't have the "1 credit per person over 30" rule.
3. I also wrote 3 more tests in test_historical.py to check the example provided (35 people = $725.00 and 7 credits), the required boundary case of audience size of 20 people = $500.00, and 21 people = $515.00, and how tragedy and comedy charges are unchanged when a histroical play is included in the same purchase.

Results:
tests/test_historical.py::test_historical_example_from_spec PASSED [ 14%]
tests/test_historical.py::test_historical_audience_boundary_at_20 PASSED [ 28%]
tests/test_historical.py::test_historical_with_original_play_types PASSED [ 42%]
tests/test_statement.py::test_example_statement PASSED [ 57%]
tests/test_statement.py::test_statement_with_new_play_types PASSED [ 71%]
tests/test_statement.py::test_tragedy_audience_boundary_at_30 PASSED [ 85%]
tests/test_statement.py::test_comedy_audience_boundary_at_20 PASSED [100%]

7 passed

## Part 5 – Documentation and Reflection

### Tools and commands

I used Python for the language, pytest, approvaltests, and pytest-approvaltests for testing (listed in requirements.txt), and these following commands to set up the virtual environment (make sure you cd into the project directory):
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -v

### Test Results

- Initial results: 2 passed (see 3. in Part 1).
- Final results: 7 passed (see 3. in Part 4).
- The new tests are explained in Part 3 (two boundary tests for existing behavior) and Part 4 (three tests for historical plays).

### My four refactored code steps

See Part 2 for the four refactoring steps.

### Reflection

I think the refactoring that helped the most was replacing the if/elif on play type with classes (polymorphism). In the original code, the play type was checked in two places, once for the price and once for the credits. So the rules for tragedy and comedy were spread out and mixed together. Now each play type has its own class with all of its rules in one place. The rest of the code just calls amount() and volume_credits() and doesn't need to know what type of play it is. Splitting the calculations from the formatting also helped a lot, because it made this step much easier to do, but the classes are what made the code easy to add to.

Refactoring is different from adding functionality because when you refactor, the program should do exactly the same thing as before. You are only changing how the code is organized. One example of this in my project was the comedy credits. The original comment said comedy gives extra credit for "every ten" people, but the code actually divides by 5. It looked like a bug, but I kept it as 5 because changing it would change the output, and then it wouldn't be refactoring anymore. If it is a bug, it should be fixed as a separate change with updated tests. Adding historical plays was different because the whole point was to change what the program does, so I did it after the refactoring was done and wrote new tests for it.

The new design made adding historical plays pretty easy. I only had to add a HistoricalCalculator class and one more if statement in create_performance_calculator. I didn't have to change the tragedy, comedy, or formatting code, so I wasn't worried about breaking anything. The one thing I had to think about was the credits. Historical plays don't get the normal "1 credit per person over 30", so HistoricalCalculator has its own volume_credits() instead of using the one from the base class. With the original code, I would have had to add another branch to both if/elif blocks and make sure it didn't mess up the comedy credit check.

For the problems I found in Part 1, the long statement function is fixed since each part now does one thing. The confusing money numbers are only partly fixed. They are still in cents, but now each one is inside a class with a clear name, so it's easier to tell what it's for. The dictionaries with string keys are not fixed. I left them because the tests and JSON files use them, but changing them to a class or dataclass would be a good next step.

### Attribution

- Original repository: Theatrical Players Refactoring Kata by Emily Bache, https://github.com/emilybache/Theatrical-Players-Refactoring-Kata, based on the first chapter of Martin Fowler's Refactoring (2nd edition).
- Sky Zheng
- October 20, 2026
- I refactored statement.py into two separate modules: create_statement_data.py for calculations and statement.py for formatting text outputs, replaced the if/else conditionals with calculator classes (polymorphism), added two boundary tests, and added three more tests for the "historical" play type.

### Use of Generative AI

I used Claude (Anthropic) to help me understand Fowler's refactoring steps, understand coding techniques, help debug, generate mock data for "historical" play type, and draft parts of this README documentation. I reviewed every change, wrote the refactored code, ran the tests after each step, and made sure I understood the design decisions.
