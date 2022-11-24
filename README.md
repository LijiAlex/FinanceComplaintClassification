# FinanceComplaintClassification
Classify the complaints registered at https://www.consumerfinance.gov/ as malicious (the one which requires immediate attention) and non malicious

## Strategies
* Use pyspark
* Download data from website in parts
* Convert data files to parquet format since the data is huge.

### Transformation Strategies
* Generate a new feature ['diff_in_days'].
* Impute values in ['diff_in_days'] using mean.
* Impute the missing values of ['company_response', 'consumer_consent_provided', 'submitted_via'] with most frequent items.
* Transform ['company_response', 'consumer_consent_provided', 'submitted_via'] using string indexer.
* Transform ['company_response', 'consumer_consent_provided', 'submitted_via'] using one hot encoder.
* Tokenize ['issue']
* Hash the tokenized words.
* Create transformed issue column using IDF
* Apply vector assembler on all transformed columns
* Apply standard scalar to assembled column

