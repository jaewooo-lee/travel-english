#!/bin/bash

# 에러 발생 시 즉시 스크립트 중단
set -e

IMAGE_NAME="jaewooo/travel-english"
TAG="latest"

echo "=================================================="
echo "🚀 Travel English (Python Pure) Docker Build Starting"
echo "=================================================="

# 1. buildx 빌더 환경 생성 및 사용 설정
echo "⚙️  Checking and creating buildx builder..."
if ! docker buildx inspect travel-builder > /dev/null 2>&1; then
    docker buildx create --name travel-builder --driver docker-container --use
else
    docker buildx use travel-builder
fi

# 빌더 활성화 및 확인
docker buildx inspect --bootstrap

# 2. 멀티 아키텍처 빌드 및 이미지 푸시 실행
# (linux/amd64와 linux/arm64 아키텍처를 동시 빌드하여 jaewooo/travel-english 레포지토리로 push)
echo "📦 Building and pushing Python unified Docker image: ${IMAGE_NAME}:${TAG}..."
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t "${IMAGE_NAME}:${TAG}" \
    --push \
    .

echo "=================================================="
echo "🎉 Multi-architecture Docker image successfully built and pushed!"
echo "=================================================="
