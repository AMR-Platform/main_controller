#!/usr/bin/env bash
set -e

# names for the concrete images
ARM_TAG=myrepo/ros-dev-arm64
AMD_TAG=myrepo/ros-dev-amd64

# ── 1. Build / push the Jetson variant  ───────────────────
docker buildx build --platform linux/arm64 \
  --build-arg BASE=dustynv/ros:humble-desktop-l4t-r32.7.1 \
  -t $ARM_TAG --push .

# ── 2. Build / push the PC variant (run this on the laptop) ─
docker buildx build --platform linux/amd64 \
  --build-arg BASE=osrf/ros:humble-desktop \
  -t $AMD_TAG --push .

# ── 3. Stitch them together under one manifest tag ─────────
docker manifest create  myrepo/ros-dev:latest \
       --amend $ARM_TAG \
       --amend $AMD_TAG

docker manifest push    myrepo/ros-dev:latest
