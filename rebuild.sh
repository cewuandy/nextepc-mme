#/bin/bash
docker build -t cewuandy/nextepcmme-synchronizer -f Dockerfile.synchronizer .
docker push cewuandy/nextepcmme-synchronizer

