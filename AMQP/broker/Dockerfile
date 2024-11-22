#example of rabbit mq docker config with oauth enabled

FROM rabbitmq:3-management

# Define user and password (temporary)
ENV RABBITMQ_DEFAULT_USER=admin
ENV RABBITMQ_DEFAULT_PASS=admin

RUN rabbitmq-plugins enable rabbitmq_management

# # Enable plugins 
# RUN rabbitmq-plugins enable rabbitmq_auth_backend_oauth2 #For later use

# # Copy custom RabbitMQ configuration file (if needed)
# COPY rabbitmq.conf /etc/rabbitmq/

# # Copy definitions file to preload exchanges, queues, users, etc.
# COPY definitions.json /etc/rabbitmq/

# Expose RabbitMQ default ports
EXPOSE 5672 15672

# Set the entry point to start RabbitMQ
CMD ["rabbitmq-server"]
