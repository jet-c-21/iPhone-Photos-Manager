# iPhone-Photos-Manager

python iphone photos management tools

## Setup Environment

### python env

#### with conda

```shell
conda create --name iphone-pm python=3.12 -y
```

### install `ifuse`

```
sudo apt update && \
sudo apt install libimobiledevice-utils ifuse
```

## Qick Start

### pair iphone with `ifuse`

```shell
idevicepair pair
```

```shell
idevicepair validate
```

### create mount dir

```shell
mkdir -p ~/my_home/ifuse_iphone_link && \
ifuse ~/my_home/ifuse_iphone_link
```