RSYNC_ARGS="--progress "
VERSION=0.1.1

if [[ "$1" == "dev" ]]; then
    DEPLOY_DEV_TARGET=admin@172.31.4.85
    TARGET=/csmtec/backend-stack
    SSHTARGET=$DEPLOY_DEV_TARGET:$TARGET
    AWS_ECR_URL=637423504461.dkr.ecr.sa-east-1.amazonaws.com
    IMAGEMODE=dev
    echo "Deploying to development environment..."
elif [[ "$1" == "staging" ]]; then
    DEPLOY_DEV_TARGET=admin@172.31.0.182
    TARGET=/csmtec/backend-stack
    SSHTARGET=$DEPLOY_DEV_TARGET:$TARGET
    AWS_ECR_URL=637423504461.dkr.ecr.sa-east-1.amazonaws.com
    IMAGEMODE=staging
    echo "Deploying to development environment..."
else
    echo "Invalid argument. Use 'dev' to deploy to development environment."
    exit 1
fi

build_image() {
    IMAGE_NAME=$1
    VERSION_FILE="./scripts/$IMAGE_NAME.version"
    echo "Building image: $IMAGE_NAME"

    # Autoincrement version for this image
    if [ ! -f "$VERSION_FILE" ]; then
        echo "0.1.0" > "$VERSION_FILE"
    fi
    VERSION=$(cat "$VERSION_FILE")
    IFS='.' read -r major minor patch <<< "$VERSION"
    patch=$((patch+1))
    NEW_VERSION="$major.$minor.$patch"

    echo "$NEW_VERSION" > "$VERSION_FILE"
    VERSION="$NEW_VERSION"

    # COMPOSE_FILE="../.deploy/dev/docker-compose-dev.yml"
    # sed -i "s|\\(csmtec/$IMAGE_NAME:\\)[0-9]*\\.[0-9]*\\.[0-9]*-dev|\\1$VERSION-dev|g" "$COMPOSE_FILE"

    TAG="csmtec/$IMAGE_NAME:$VERSION-$IMAGEMODE"
    echo "Building Docker image: $TAG"

    DOCKER_FILE="${3:-Dockerfile}"
    docker build -t $TAG .
    echo "Tagging and pushing image to ECR: $AWS_ECR_URL/$TAG"
    docker tag $TAG $AWS_ECR_URL/$TAG
    docker push $AWS_ECR_URL/$TAG
    echo "Image built and pushed: $AWS_ECR_URL/$TAG"
    echo "Image $IMAGE_NAME built successfully with version $VERSION"
}

cd ../
set -e
#aws ecr get-login-password --region sa-east-1 --profile csmtec | sudo docker login --username AWS --password-stdin $AWS_ECR_URL
build_image ai-agents ../

echo "Running ai-agents image..."

ssh $DEPLOY_DEV_TARGET "
  aws ecr get-login-password --region sa-east-1 | sudo docker login --username AWS --password-stdin $AWS_ECR_URL &&
  sudo docker stop ai-agents &&
  sudo docker container prune &&
  sudo docker run -d --name ai-agents --restart unless-stopped -p 8000:8000 $AWS_ECR_URL/csmtec/ai-agents:$VERSION-$IMAGEMODE
"
