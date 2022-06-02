#!/bin/bash
docker-compose run api-container py.test tavern_tests/test_contracts.tavern.yaml -v
