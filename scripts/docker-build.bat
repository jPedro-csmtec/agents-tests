@echo off

set tag=ai-tests:1.0.17-dev
set url=637423504461.dkr.ecr.sa-east-1.amazonaws.com/csmtec/ai-agents
cd ..
docker build -t %tag% .
docker tag %tag% %url%
docker push %url%

REM Uncomment the following lines if AWS ECR login is required
REM aws ecr get-login-password --region sa-east-1 --profile csmtec | docker login --username AWS --password-stdin 637423504461.dkr.ecr.sa-east-1.amazonaws.com

REM  aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 637423504461.dkr.ecr.sa-east-1.amazonaws.com