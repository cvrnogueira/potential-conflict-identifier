Instructions used by human volunteers for conflict creation
===========================================================

The following text was used to guide the volunteers during the norm
conflict insertion. The document consists of a description for each step
of the system.

* * * * *

This README explains how to execute `create_conflicting_norms.py` to
introduce conflicts randomly in contracts from our corpus.[1] The main
goal is to create contracts containing norm conflicts independently from
a conflict detection algorithm.

**Execute:**

-   To execute, run the following command:
    `python -B create_conflicting_norms.py`

**Options:**

-   After login, there will be two initial options:

    -   Pick a random contract; and

    -   Finish.

-   This option chooses a contract from the corpus at random. This step
    may return an error due to the choice of a contract without norms;
    if that happens, ignore the error and press (1) again. If no error
    occurs, the program will display information, such as the total
    number of norms extracted and the parties identified;

-   This option just clears the output folder and exits.

-   When the user selects a contract, the program adds a new option:

    -   Pick a random contract;

    -   Pick a random norm; and

    -   Finish.

-   Option (1) restarts the process with a new contract;

-   Option (2) chooses a random norm among the extracted ones.

-   When the user selects a norm, the program adds yet another option:

    -   Pick a random contract;

    -   Pick a random norm;

    -   Make a conflict; and

    -   Finish.

-   Options (1,2,4) are the same as before;

-   Option (3) displays the last chosen norm and asks you to alter it in
    order to create a conflict.

**Process:**

-   In this manual conflict insertion, you are intended to follow a
    series of steps.

    1.  Execute `create_conflicting_norms.py`;

    2.  Insert your first name, and pick a contract with option (1);

    3.  Choose a random norm using option (2);

    4.  Choose the option to create a conflict (3).

-   You have to create between 70 and 100 conflicts of 3 types. These
    types are:

    -   Permission x Obligation (33%);

    -   Permission x Prohibition (33%);

    -   Obligation x Prohibition (33%).

-   A regular norm has the following structure:

-   **Example 1.:**

    -   “Purchaser must pay the product taxes.”

Given a regular norm, you will choose option 3, which allows you to
alter such norm. Then you have to alter it in order to generate a
conflict, e.g., if you got the Example 1, you may choose to create
either a Permission x Obligation conflict or an Obligation x
Prohibition conflict. In the first case (Permission x
Obligation), a possible modification can be described as follows:

-   **Example 2.:**

    -   “Purchaser MAY pay the product taxes.”

To ensure that you are really making a conflict, use
the following Table as a guide:

|   Modal Verb   | Deontic Meaning |
|:--------------:|:---------------:|
|       can      |    permission   |
|       may      |    permission   |
|      must      |    obligation   |
|      ought     |    obligation   |
|      shall     |    obligation   |
|      will      |    obligation   |
| modal_verb not |   prohibition   |

You may also modify the structure after the modal verb creating a
conflict and altering the conflict structure (obviously maintaining the
same meaning), as the Example 3 shows.

-   **Example 3.:**

    -   “Purchaser may choose to pay the taxes related to the product.”

-   We recommend you to use more than three contracts to create
    conflicts, it allows us to test our approach in different contexts.

-   At the end of the process, choose option (4) and that’s it!

Thanks in advance.

[1]: This code is available at
    <https://github.com/JoaoPauloAires/potential-conflict-identifier>
