# FinanceComplaintClassification
Classify the complaints registered at https://www.consumerfinance.gov/ as malicious (the one which requires immediate attention) and non malicious

## Strategies
* Use pyspark
* Download data from website in parts
* Convert data files to parquet format since the data is huge.
* Save model in S3 bucket in compressed format.

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
* Transformed file will contain only the Scaled and Assembled columns and target feature.

## Tech Stack Used
1. Python 
2. PySpark
3. PySpark ML
4. Airflow as Scheduler
5. MongoDB


## Infrastructure Required.

1. GCP Compute Engine
2. S3 Bucket
3. Artifact Registry

## Dashboarding
1. Grafana
2. Prometheus
3. Node Exporter
4. Promtail
5. Loki


