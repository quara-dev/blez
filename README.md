## Usage

- Without docker:

```bash
./scripts/build.sh 5.55 5.56 5.57 5.58 5.59 5.60 5.61 5.62 5.63 5.64 5.65 5.66
```

> By default, artifacts are located in `/opt/bluez` and each bluez version is installed in `/opt/bluez-$VERSION`.

- With docker (for cross-platform builds):

```bash
PLATFORM="linux/arm64"
./scripts/cp-build.sh "$PLATFORM" 5.55 5.56 5.57 5.58 5.59 5.60 5.61 5.62 5.63 5.64 5.65 5.66
```

> When using docker, artifacts are located in the `dist/` directory.

## Solidrun Runtime Environments

In order to run Bluetooth stack on Solidrun devices, it is recommended to use the image built from:

> https://github.com/SolidRun/imx6_buildroot
