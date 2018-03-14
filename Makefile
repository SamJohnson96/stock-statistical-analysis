PROJECT = stock_statistical_analysis
AWS_REGION = eu-west-2
LAMBDA_ROLE = arn:aws:iam::329627156298:role/service-role/lambda_basic

# COLLECT APPLE  RESULTS FUNCTION
UPDATE_APPLE_PREDICTION_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:UpdateApplePrediction
UPDATE_APPLE_PREDICTION_FILE_NAME = update-apple-prediction
UPDATE_APPLE_PREDICTION_FUNCTION_HANDLER = lambda_handler

# COLLECT FACEBOOK RESULTS FUNCTION
UPDATE_FACEBOOK_PREDICTION_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:UpdateFacebookPrediction
UPDATE_FACEBOOK_PREDICTION_FILE_NAME = update-facebook-prediction
UPDATE_FACEBOOK_PREDICTION_FUNCTION_HANDLER = lambda_handler

# COLLECT TECHNOLOGY RESULTS FUNCTION
UPDATE_TECHNOLOGY_PREDICTION_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:UpdateTechnologyPrediction
UPDATE_TECHNOLOGY_PREDICTION_FILE_NAME = update-technology-prediction
UPDATE_TECHNOLOGY_PREDICTION_FUNCTION_HANDLER = lambda_handler

# BUILD AND CREATE PACKAGES
build_update_apple_prediction: clean_package organise_update_apple_prediction
build_update_facebook_prediction: clean_package organise_update_facebook_prediction
build_update_technology_prediction: clean_package organise_update_technology_prediction

# BUILD - DELETE - CREATE
refresh_update_apple_prediction: build_update_apple_prediction update_apple_prediction_delete update_apple_prediction_create
refresh_update_facebook_prediction: build_update_facebook_prediction update_facebook_prediction_delete update_facebook_prediction_create
refresh_update_technology_prediction: build_update_technology_prediction update_technology_prediction_delete update_technology_prediction_create

refresh_all_predictions: refresh_update_apple_prediction refresh_update_facebook_prediction refresh_update_technology_prediction

# CLEAN BUILD
clean_package:
	# Clean the build folder
	sudo rm -rf build

# DOWNLOAD ALL PACKAGES AND FILES NEEDED FOR DEPLOYMENT FOR METHODS
organise_update_apple_prediction:
	# Make site-packages
	mkdir -p build/site-packages

	# Move
	cp stock_statistical_analysis/update_apple_prediction.py build/site-packages

	# Create virtual environment in build/scrape
	virtualenv -p /usr/bin/python3.4 build/update-apple-prediction

	# Activate the virtual environment
	. build/update-apple-prediction/bin/activate; \

  # Move to build/site-packages
	cd build/site-packages; zip -g -r ../update-apple-prediction.zip . -x "*__pycache__*"

organise_update_facebook_prediction:
	# Make site-packages
	mkdir -p build/site-packages

	# Move
	cp stock_statistical_analysis/update_facebook_prediction.py build/site-packages

	# Create virtual environment in build/scrape
	virtualenv -p /usr/bin/python3.4 build/update-facebook-prediction

	# Activate the virtual environment
	. build/update-facebook-prediction/bin/activate; \

  # Move to build/site-packages
	cd build/site-packages; zip -g -r ../update-facebook-prediction.zip . -x "*__pycache__*"

organise_update_technology_prediction:
	# Make site-packages
	mkdir -p build/site-packages

	# Move
	cp stock_statistical_analysis/update_technology_prediction.py build/site-packages

	# Create virtual environment in build/scrape
	virtualenv -p /usr/bin/python3.4 build/update_technology_prediction

	# Activate the virtual environment
	. build/update_technology_prediction/bin/activate; \

  # Move to build/site-packages
	cd build/site-packages; zip -g -r ../update_technology_prediction.zip . -x "*__pycache__*"

# CREATION AWS CLI CALLS FOR EVERY METHOD.
update_apple_prediction_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role $(LAMBDA_ROLE) \
		--function-name $(UPDATE_APPLE_PREDICTION_FUNCTION_NAME) \
		--zip-file fileb://./build/update-apple-prediction.zip \
		--handler $(UPDATE_APPLE_PREDICTION_FILE_NAME).$(UPDATE_APPLE_PREDICTION_FUNCTION_HANDLER) \
		--runtime python3.6 \
		--timeout 15 \
		--memory-size 128

update_facebook_prediction_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role $(LAMBDA_ROLE) \
		--function-name $(UPDATE_FACEBOOK_PREDICTION_FUNCTION_NAME) \
		--zip-file fileb://./build/update-apple-prediction.zip \
		--handler $(UPDATE_FACEBOOK_PREDICTION_FILE_NAME).$(UPDATE_FACEBOOK_PREDICTION_FUNCTION_HANDLER) \
		--runtime python3.6 \
		--timeout 15 \
		--memory-size 128

update_technology_prediction_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role $(LAMBDA_ROLE) \
		--function-name $(UPDATE_TECHNOLOGY_PREDICTION_FUNCTION_NAME) \
		--zip-file fileb://./build/update-apple-prediction.zip \
		--handler $(UPDATE_TECHNOLOGY_PREDICTION_FILE_NAME).$(UPDATE_TECHNOLOGY_PREDICTION_FUNCTION_HANDLER) \
		--runtime python3.6 \
		--timeout 15 \
		--memory-size 128

# DELETION AWS CLI CALLS FOR EVERY METHOD
update_apple_prediction_delete:
	aws lambda delete-function \
		--function-name $(UPDATE_APPLE_PREDICTION_FUNCTION_NAME)

update_facebook_prediction_delete:
	aws lambda delete-function \
		--function-name $(UPDATE_FACEBOOK_PREDICTION_FUNCTION_NAME)

update_technology_prediction_delete:
	aws lambda delete-function \
		--function-name $(UPDATE_TECHNOLOGY_PREDICTION_FUNCTION_NAME)

run_all_tests:
	python3 -m unittest tests/test_alpha_vantage_wrapper.py
	python3 -m unittest tests/test_marker.py
	python3 -m unittest tests/test_prediction_wrapper.py
	python3 -m unittest tests/test_results_to_db.py
	python3 -m unittest tests/test_stock_calculator.py
