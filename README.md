# Plugins for telegraf & collectd

# noaa.py

It's a plugin for read the nhc noaa rss and save into influx, have another function to get link of the storm. [Grafana Dashboard.](https://github.com/c0reyes/telegraf_collectd_plugins/blob/master/dashboards/noaa.json)

## Settings

```
[[inputs.exec]]
  commands = ["python3 noaa.py -u https://www.nhc.noaa.gov/index-cp.xml"]
  data_format = "influx"
  interval = "3600s"
  timeout = "90s"

[[inputs.exec]]
  commands = ["python3 noaa.py -u https://www.nhc.noaa.gov/index-at.xml"]
  data_format = "influx"
  interval = "3600s"
  timeout = "90s"

[[inputs.exec]]
  commands = ["python3 noaa.py -u https://www.nhc.noaa.gov/index-ep.xml"]
  data_format = "influx"
  interval = "3600s"
  timeout = "90s"
```

## Requirements

Python libs:

- BeautifulSoup

# huawei_telegraf.py

This plugins tested with Huawei HG8245H. Get the info necesary for the graph. Use with telegraf exec plugin.

## Settings

```
[[inputs.exec]]
  commands = ["python huawei_telegraf.py -u <username> -p <password> -i <ip>"]
  name_suffix = "_huawei"
  data_format = "influx"
  interval = "120s"
  timeout = "20s"
```

## Requirements

Python libs:

- urllib3

# huawei_collectd.py

It's the same than huawei_telegraf.py but work with collectd.

## Settings

```
LoadPlugin python

<Plugin python>
    ModulePath "/path/scripts"
    Import "huawei_collectd"
    <Module huawei_collectd>
        username "username"
        password "password"
        host "ip"
    </Module>
</Plugin>
```

## Requirements

Python libs:

- urllib3
- collectd

# transmission_telegraf.py

This script its for get the info from transmission server.

## Settings

```
[[inputs.exec]]
  commands = ["python transmission_telegraf.py -u admin -p admin -i 127.0.0.1 -x 9090"]
  data_format = "influx"
  interval = "120s"
  timeout = "20s"
```

## Requirements

Python libs:

- transmission-rpc
