# pkg-libpostal
RPM packaging of libpostal for Sailfish

To build and install:

```
export SFARCH=armv7hl
mb2 -t SailfishOS-$SFARCH -s ../pkg-libpostal/rpm/libpostal.spec build
sb2 -t SailfishOS-$SFARCH -m sdk-install -R rpm -Uvh ../rpms/devel/libpostal-devel*$SFARCH.rpm
```
