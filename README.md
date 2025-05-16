# Jetson Nano Setup for Mercusys MW600UH Adapter with ROS2 & Docker GUI

This guide details the setup of a Jetson Nano (Ubuntu 18.04) to use the Mercusys MW600UH Wi-Fi adapter, configure Ethernet interfaces for Lidar use, and deploy a ROS2 Docker container with GUI support for Lakibeam ROS drivers.

---

## Initial System Preparation

### Update & Install Essential Tools

```bash
sudo apt update
sudo apt upgrade
sudo apt install build-essential dkms git linux-headers-$(uname -r)
sudo apt install nvidia-l4t-kernel-headers
```

### SSH Server Configuration

```bash
sudo apt install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

---

## Mercusys MW600UH Adapter Setup

### Clone & Build RTL8192EU Driver

```bash
cd ~
git clone https://github.com/Mange/rtl8192eu-linux-driver.git
cd rtl8192eu-linux-driver

# Fix recursive variable issue
sed -i '/EXTRA_CFLAGS += $(ccflags-y)/d' Makefile

sudo dkms remove rtl8192eu/1.0 --all || true
sudo ARCH=arm64 dkms add .
sudo ARCH=arm64 dkms install rtl8192eu/1.0

sudo modprobe 8192eu
```

### Verify Wi-Fi Adapter

```bash
ip link show | grep -E 'wlan|wlx'
nmcli device wifi list
```

---

## Ethernet Port Configuration (Temporary - Repeat After Restart)

Assign Ethernet IP manually for direct Lidar communication:

```bash
sudo ip addr flush dev eth0
sudo ip addr add 192.168.198.1/24 dev eth0
sudo ip link set eth0 up
```

**Note:** This configuration must be repeated after each reboot.

---

## Docker Image Build via Dockerfile

Instead of manually running lengthy `docker run` commands, you can build a **custom Docker image** that automates our entire ROS2 + Lakibeam setup. Include the following `Dockerfile` in your GitHub repo alongside this README:

```dockerfile
# Dockerfile for Jetson Nano ROS2 + Lakibeam Setup
FROM dustynv/ros:humble-desktop-l4t-r32.7.1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y \
      build-essential \
      git \
      python3-colcon-common-extensions && \
    rm -rf /var/lib/apt/lists/*

# Create and initialize ROS2 workspace
ENV ROS_WS=/workspace/ros2_ws
RUN mkdir -p $ROS_WS/src
WORKDIR $ROS_WS/src

# Clone the Lakibeam ROS2 driver
RUN git clone https://github.com/RichbeamTechnology/Lakibeam_ROS2_Driver.git

# Build the workspace
WORKDIR $ROS_WS
RUN . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install && \
    rm -rf build log install

# Source ROS2 and workspace at container start
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source $ROS_WS/install/setup.bash" >> ~/.bashrc

# Default entrypoint
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
```

### Building your custom image

From the root of your cloned repository (with the `Dockerfile` present), run:

```bash
# Build and tag your image
docker build -t ros_dev_custom:latest .
```

## ROS2 Docker Container with GUI Setup

### Allow Docker X11 Forwarding (Temporary - Repeat After Restart)

After each system restart, run:

```bash
xhost +local:root
```


### Running containers from your image

Use the same GUI-friendly flags, but replace the image name:

```bash
docker run -it \
  --network host \
  --privileged \
  -e DISPLAY=$DISPLAY \
  -e XAUTHORITY=$XAUTHORITY \
  -e QT_X11_NO_MITSHM=1 \
  -e QT_QPA_PLATFORM=xcb \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $XAUTHORITY:/root/.Xauthority:ro \
  --device /dev/dri \
  --gpus all \
  ros_dev_custom:latest
```

This single command spins up a container already pre-configured with ROS2 Humble, the Lakibeam driver, and your workspace.

## Lakibeam ROS2 Driver Setup in Container

Inside the container terminal:

### Clone & Build Lakibeam ROS2 Driver

```bash
mkdir -p ~/main_controller/src
cd ~/main_controller/src
git clone https://github.com/RichbeamTechnology/Lakibeam_ROS2_Driver.git
cd ..
colcon build
source install/setup.bash
```

### Run Lidar Launch Files

```bash
# Run LaserScan node continuously in the background
ros2 launch lakibeam1 lakibeam1_scan.launch.py > scan.log 2>&1 &

# View point cloud in RViz
ros2 launch lakibeam1 lakibeam1_scan_view.launch.py
```

---

## Troubleshooting GUI Issues

If the Docker GUI connection fails, repeat the following after each host reboot:

```bash
xhost +local:root
```

Ensure that the Docker container is started with appropriate X11 bindings (see Docker Container Launch above).

---

## Summary of Actions Needed After Each Restart

* **Ethernet configuration:**

```bash
sudo ip addr flush dev eth0
sudo ip addr add 192.168.198.1/24 dev eth0
sudo ip link set eth0 up
```

* **Docker GUI X11 Access:**

```bash
xhost +local:root
```

This ensures the system is ready for direct Lidar communication and Docker GUI access after every reboot.