# telegraf & collectd - plugins

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
