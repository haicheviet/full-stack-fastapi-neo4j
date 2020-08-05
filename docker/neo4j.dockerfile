FROM neo4j:3.5.14

COPY movie_data ./movie_data

COPY wrapper.sh wrapper.sh
COPY initial-data.sh initial-data.sh

RUN chmod +x initial-data.sh
RUN chmod +x wrapper.sh

ENTRYPOINT ["./wrapper.sh"]