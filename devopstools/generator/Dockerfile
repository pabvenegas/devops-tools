FROM centos:centos7

ARG PRODUCT_VERSION

COPY files /
COPY tests tests

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["main"]