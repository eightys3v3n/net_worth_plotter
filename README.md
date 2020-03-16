# Idea
This project is intended to visualize my net worth over time. Net worth would be
calculated based on a number of things: bank statements, credit statements, investment
statements. Some of these statements would need to be generated based on things like
the historic price of silver. Therefore the statement importer must be modular. The
Transaction type will also have to be capable of handling many kinds of statements.


# Current status
It is currently not working correctly because my plot first_calgary module (the first module)
needs to fill in balances for days that don't have one (see First Calgary Credit Union).

## Aliases
Allows the renaming of accounts for ease of reading.
Put a JSON output into aliases.json containing {"source account name": "what you want it to be"}


## Supported statements
### First Calgary Credit Union
- The statements must have been exported in (Oldest to newest) mode which gives a CSV.
- All exported CSV statements should go in `statements/first_calgary`. All CSV files will be read and
	duplicates removed.
- One can export any number of statements for different accounts or date ranges. Missing days from
	the global date range will be derived.
- Since the bank only gives transactions rather than daily balances, we must derive the daily balances
	based on transaction details. Assumed to be $0 if there are no records that old, or carry the last
	balance if there are no reconds that new.

# ToDo
- Add a file to allow drawing of verticle lines on graph for important dates. Things like holidays,
   starting new jobs, ending jobs and so on.
- Implement more statement modules (BMO credit card, CTFS credit card, XRP value based on given coin amount,
   silver value based on given amount, large purchases and depreciation)
- Put statement modules in a modules directory. I haven't done this because I don't know how to properly
   structure folders in a Python project such that they can use functions in the parent folder.


## Versions
- dbe72a5e38b6aa189199866938ff6a0641c9b7ca:
	Before refactor
- d417120705d3ee1996163f932b67137f63858426:
	After refactor
	Modularized importing of data points. Fixed data interp
- 4ae863661adee8f640c0682add8e8c86e372e520
	Switched to plotly for graphing.
