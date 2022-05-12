<br />
<div align="center">
  <h1 align="center">Unit Reconciliation</h1>
</div>


<br />

<!-- ABOUT THE PROJECT -->
## About The Project

Reconciliation is a term used for a set of correctness and consistency measures applied to data received and used in financial calculations. One of the most common reconciliation checks is called *unit reconciliation*, which answers the question, "does the transaction history add up to the number of shares the bank says I have?". For example, if the bank said I had 100 shares of Apple at the end of yesterday, and I bought 20 shares of Apple today, then we expect the bank to report 120 shares at the end of today. This surprisingly isn't always the case! The bank may send incomplete data, we may be parsing it incorrectly, or there may be events like corporate actions or trade settlement lag that cause an inconsistency.

<br />

<!-- GETTING STARTED -->
## Getting Started

Please follow these simple steps to get a local copy up and running.


### Prerequisites

This program was tested with Python 3.8.


### Installation

1. Clone the repo
   ```sh
   $ git clone https://github.com/shmuelhertz/unit_reconciliation.git
   ```
2. Install requirements.txt packages
   ```sh
   $ pip install -r requirements.txt
   ```


<br />

<!-- USAGE EXAMPLES -->
## Usage
* After installation place your data in a file and name it `recon.in`. (A sample file is provided.) 
* Make sure that [`recon.in`](https://github.com/shmuelhertz/unit_reconciliation/blob/main/recon.in) is in the same directory as [`unit_reconciliation.py`](https://github.com/shmuelhertz/unit_reconciliation/blob/main/unit_reconciliation.py). 

* Run the script in your terminal. The script will automatically generate a `recon.out` file with the reconciliation result. 

```sh
python unit_reconciliation.py
```

<br />

## Example 

In recon.in
  ```sh
  D0-POS
  AAPL 100
  GOOG 200
  SP500 175.75
  Cash 1000

  D1-TRN
  AAPL SELL 100 30000
  GOOG BUY 10 10000
  Cash DEPOSIT 0 1000
  Cash FEE 0 50
  GOOG DIVIDEND 0 50
  TD BUY 100 10000

  D1-POS
  GOOG 220
  SP500 175.75
  Cash 20000
  MSFT 10
  ```

Run:
  ```sh
  python unit_reconciliation.py
  ```

In recon.out
  ```sh
  Cash 8000
  GOOG 10
  MSFT 10
  TD -100
  ```