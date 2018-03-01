PROJECT = stock_statistical_analysis
AWS_REGION = eu-west-2
LAMBDA_ROLE = arn:aws:iam::329627156298:role/service-role/lambda_basic

# COLLECT RESULTS FUNCTION
COLLECT_RESULTS_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:CollectResults
COLLECT_RESULTS_FILE_NAME = collect_results
COLLECT_RESULTS_FUNCTION_HANDLER = lambda_handler

# BUILD AND CREATE PACKAGES
build_collect_results: clean_package organise_collect_results

# BUILD - DELETE - CREATE
refresh_naive_bayes: build_collect_results collect_results_delete collect_results_create:

# CLEAN BUILD
clean_package:
	# Clean the build folder
	sudo rm -rf build

# DOWNLOAD ALL PACKAGES AND FILES NEEDED FOR DEPLOYMENT FOR METHODS
organise_collect_results:
	# Make site-packages
	mkdir -p build/site-packages

	# Move
	cp stock-statistical-analysis/collect_results.py build/site-packages

	# Create virtual environment in build/scrape
	virtualenv -p /usr/bin/python3.4 build/collect_results

	# Activate the virtual environment
	. build/collect_results/bin/activate; \

	# Install dependencies in virtual environment
	# sudo python3 -m pip install -U requests -t build/site-packages/
	# sudo python3 -m pip install -U boto3 -t build/site-packages/

  # Move to build/site-packages
	cd build/site-packages; zip -g -r ../collect_results.zip . -x "*__pycache__*"

# CREATION AWS CLI CALLS FOR EVERY METHOD.
collect_results_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role $(LAMBDA_ROLE) \
		--function-name $(COLLECT_RESULTS_FUNCTION_NAME) \
		--zip-file fileb://./build/naive_bayes.zip \
		--handler $(COLLECT_RESULTS_FILE_NAME).$(COLLECT_RESULTS_FUNCTION_HANDLER) \
		--runtime python3.6 \
		--timeout 15 \
		--memory-size 128

# DELETION AWS CLI CALLS FOR EVERY METHOD
collect_results_delete:
	aws lambda delete-function \
		--function-name $(COLLECT_RESULTS_FUNCTION_NAME)
