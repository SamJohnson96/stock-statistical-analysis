PROJECT = stock_statistical_analysis
AWS_REGION = eu-west-2
LAMBDA_ROLE = arn:aws:iam::329627156298:role/service-role/lambda_basic

# COLLECT RESULTS FUNCTION
UPDATE-APPLE-PREDICTION_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:UpdateApplePrediction
UPDATE-APPLE-PREDICTION_FILE_NAME = update-apple-prediction
UPDATE-APPLE-PREDICTION_FUNCTION_HANDLER = lambda_handler

# BUILD AND CREATE PACKAGES
build_update-apple-prediction: clean_package organise_update-apple-prediction

# BUILD - DELETE - CREATE
refresh_update-apple-prediction: build_update-apple-prediction update-apple-prediction_delete update-apple-prediction_create

# CLEAN BUILD
clean_package:
	# Clean the build folder
	sudo rm -rf build

# DOWNLOAD ALL PACKAGES AND FILES NEEDED FOR DEPLOYMENT FOR METHODS
organise_update-apple-prediction:
	# Make site-packages
	mkdir -p build/site-packages

	# Move
	cp stock-statistical-analysis/update-apple-prediction.py build/site-packages

	# Create virtual environment in build/scrape
	virtualenv -p /usr/bin/python3.4 build/update-apple-prediction

	# Activate the virtual environment
	. build/update-apple-prediction/bin/activate; \

	# Install dependencies in virtual environment
	# sudo python3 -m pip install -U requests -t build/site-packages/
	# sudo python3 -m pip install -U boto3 -t build/site-packages/

  # Move to build/site-packages
	cd build/site-packages; zip -g -r ../update-apple-prediction.zip . -x "*__pycache__*"

# CREATION AWS CLI CALLS FOR EVERY METHOD.
update-apple-prediction_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role $(LAMBDA_ROLE) \
		--function-name $(UPDATE-APPLE-PREDICTION_FUNCTION_NAME) \
		--zip-file fileb://./build/update-apple-prediction.zip \
		--handler $(UPDATE-APPLE-PREDICTION_FILE_NAME).$(UPDATE-APPLE-PREDICTION_FUNCTION_HANDLER) \
		--runtime python3.6 \
		--timeout 15 \
		--memory-size 128

# DELETION AWS CLI CALLS FOR EVERY METHOD
update-apple-prediction_delete:
	aws lambda delete-function \
		--function-name $(UPDATE-APPLE-PREDICTION_FUNCTION_NAME)
