import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import yaml

# Read the YAML configuration
with open('glue_job_config.yaml', 'r') as yaml_file:
    job_config = yaml.safe_load(yaml_file)

# Initialize Spark and Glue contexts
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Read data from CSV based on the YAML configuration
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="your_database_name",
    table_name="your_table_name",
    transformation_ctx="datasource"
)

# Rename columns to match Salesforce field names
for old_name, new_name in job_config.get("column_renaming", {}).items():
    datasource = datasource.rename_field(old_name, new_name)

# Perform any additional transformations as needed

# Write the data to Salesforce
glueContext.write_dynamic_frame.from_catalog(
    frame=datasource,
    database="your_salesforce_database",
    table_name="your_salesforce_table",
    transformation_ctx="datasink"
)

job.commit()
