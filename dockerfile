FROM ppodgorsek/robot-framework

USER root

RUN pip3 install --no-cache-dir boto3

RUN pip3 install jproperties

COPY elementfinder.py /usr/local/lib/python3.8/site-packages/SeleniumLibrary/locators/
