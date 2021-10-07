# OSIx > Modules > Bitcoin Wallet & Transacations

This module enables to Download a Single Bitcoin Wallet Information and Transactions and to export the Bitcoin Transactions Graph to Gephi or GraphML files.

### Exported Files

The exportation process always generate 3 distinct files:

 * btc_wallet_all_BTCWalletId.extension - Includes all Transactions
 * btc_wallet_inputs_BTCWalletId.extension - Only the Input Transactions
 * btc_wallet_outputs_BTCWalletId.extension - Only the Output Transactions

### Basic Command Line

```bash
python3 -m OSIx --btc_wallet 1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3 --btc_get_transactions
``` 

 * **--btc_wallet** - Target Bitcoin Wallet
 * **--btc_get_transactions** - Allow the Executor to Download All Transactions from the Target Bitcoin Waller
 
 ### Export Options
 
  * **--export_btc_transactions_as_graphml** - Export the Graphs as [GraphML](https://en.wikipedia.org/wiki/GraphML)
  * **--export_btc_transactions_as_gephi** - Export the Graphs as [Gephi](https://gephi.org/) File
  
 ---
 
 [<< BACK](../README.md)