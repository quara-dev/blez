## Usage

### Building Docker Images

All Dockerfiles support a `PYTHON_VERSION` build arg (defaults to `3.12`).

```bash
# Build base image (Python 3.12, default)
docker build -f Dockerfile.base -t quara/blez-base:3.12 .

# Build base image (Python 3.10)
docker build -f Dockerfile.base --build-arg PYTHON_VERSION=3.10 -t quara/blez-base:3.10 .

# Build build image (Python 3.12, default)
docker build -f Dockerfile.build -t quara/blez-build:3.12 .

# Build build image (Python 3.10)
docker build -f Dockerfile.build --build-arg PYTHON_VERSION=3.10 -t quara/blez-build:3.10 .

# Build final image (Python 3.12, default)
docker build -t quara/blez:3.12 .

# Build final image (Python 3.10)
docker build --build-arg PYTHON_VERSION=3.10 -t quara/blez:3.10 .
```

### Building BlueZ

- Without docker:

```bash
./scripts/build.sh 5.55 5.56 5.57 5.58 5.59 5.60 5.61 5.62 5.63 5.64 5.65 5.66 5.85
```

> By default, artifacts are located in `/opt/bluez` and each bluez version is installed in `/opt/bluez-$VERSION`.

- With docker (for cross-platform builds):

```bash
PLATFORM="linux/arm64"
./scripts/cp-build.sh "$PLATFORM" 5.55 5.56 5.57 5.58 5.59 5.60 5.61 5.62 5.63 5.64 5.65 5.66 5.85
```

> When using docker, artifacts are located in the `dist/` directory.
