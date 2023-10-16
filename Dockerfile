FROM python:3

COPY anova_test 
RUN python anova_test/setup.py install 

