FROM public.ecr.aws/lambda/python:3.9

COPY lambda_requirements.txt  .
RUN  pip3 install -r lambda_requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY app.py ${LAMBDA_TASK_ROOT}
COPY src src

CMD [ "app.execute" ]