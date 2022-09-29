This example shows a complex project that involves multiple maps being
generated with shared map properties.

This features 4 different projects:

- **sensor** - A temperature sensor that exposes many parameters for engineers
to tune for performance.
Exposes only a subset of user parameters for other devices to read.
- **sa** - A standalone device that includes the sensor as well as additional
communication interface.
- **mp1** - A data acquisition device that collects information from 6
sensors.
- **mp2** - A data acquisition device that collects information from 12
sensors.
