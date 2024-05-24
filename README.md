# ML model integration for homeassistant

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
[![License][license-shield]](LICENSE.md)

![Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![Donate](https://img.shields.io/badge/donate-BuyMeCoffee-yellow.svg)](https://www.buymeacoffee.com/bigmoby)

This is a platform for interacting with a ML model under [TODO] component of Home Assistant.

## Installation

### Manual

1. Create this directory path `custom_components/ml_model/` if it does not already exist.

2. Download the all `custom_components/ml_model/` files from the repo and place it in the directory mentioned in previous step.

### HACS

1. Add this repository to HACS:

```
https://github.com/bigmoby/ml_model_component
```

2. Search for the `ML model for homeassistant` integration and choose install.

3. Reboot Home Assistant.

### Usage:

In Home Assistant->Settings->Device & services->Integration menu add the new integration ML model and configure it.

### How to test it

1. Add an MQTT integration for an already configured mqtt running broker.

2. Send a MQTT message with this payload `1,2,3` to this topic `home-assistant/ml_model`.

3. Read in `ml_model.model_outcome` sensor state the model outcome.

[releases-shield]: https://img.shields.io/github/release/bigmoby/ml_model_component.svg
[releases]: https://github.com/bigmoby/ml_model_component/releases
[project-stage-shield]: https://img.shields.io/badge/project%20stage-production%20ready-brightgreen.svg
[license-shield]: https://img.shields.io/github/license/bigmoby/ml_model_component
[maintenance-shield]: https://img.shields.io/maintenance/yes/2024.svg
[commits-shield]: https://img.shields.io/github/commit-activity/y/bigmoby/ml_model_component.svg
[commits]: https://img.shields.io/github/commits/bigmoby/ml_model_component
