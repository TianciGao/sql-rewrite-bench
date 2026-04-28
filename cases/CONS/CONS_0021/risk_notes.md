# Risk Notes

- The main subtlety is NULL versus zero handling around scalar sums over empty inputs, so the witness intentionally includes one row with no matches on either branch.
