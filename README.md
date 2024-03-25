# PowerStat's Ansible FBAHA

This is a minimal Ansible Playbook/Module implementation of the FritzBox AHA API.

See:

* [AVM Entwicklungssupport](https://avm.de/service/schnittstellen/) (1.61 2023-09-18)

Please note that I am not related to AVM in any way and that AVM will not support this code in any way!

## Installation

Because this library is only useful for ansible developers the installation depends on your ansible environment.

You need to have your modules somewhere like the 'modules' directory. And this has to be copnfigures in your 'ansible.cfg'.
Also you should have a 'playbooks' directory where you could place the 'fbaha.yaml'

## Usage

Please note that you need to have an account with username within your Fritz!Box, this will not work without a username! 
Also please note that you can find a detailed description of the commands and their parameters within the above mentioned AVM documentation!

    ansible-playbook playbooks/fbaha.yml -e fbuser=<fbUser> -e fbpasswd=<fbPassword> -e ain=<000000000000> -t "<tagname>"

The login and logout tasks are always executed! So you only need to give a tag name for the task you want to execute like 'setswitchon' including it's required parameters.

The following tags are available:

Without parameters:

- getswitchlist
- getdevicelistinfos
- gettriggerlistinfos
- gettemplatelistinfos
- getcolordefaults
- startulesubscription
- getsubscriptionstate

With only an "ain" as parameter (define with -e ain=000000000000):

- setswitchon
- setswitchoff
- setswitchtoggle
- getswitchstate
- getswitchpresent
- getswitchpower
- getswitchenergy
- getswitchname
- gettemperature
- gethkrtsoll
- gethkrkomfort
- gethkrabsenk
- getbasicdevicestats
- applytemplate
- getdeviceinfos

With individual parameters (define with -e parameter name = value; for more see AVMs mentioned documentation):

- sethkrsoll
  ain, hkrsoll

- settriggeractive
  active

- setsimpleonoff
  ain, onoff

- setlevel
  ain, level

- setlevelpercentage
  ain,level

- setcolor
  ain, hue, saturation, duration

- setunmappedcolor
  ain, hue, saturation, duration

- setcolortemperature
  ain, temperature, duration

- addcolorleveltemplate
  name, levelPercentage, hue, saturation, temperature, colorpreset

- sethkrboost
  ain, endtimestamp

- sethkrwindowopen
  ain, endtimestamp

- setblind
  ain, target

- setname
  ain, name

- setmetadata
  ain, metadata

Last but not least the 'server' name is set as 'fritz.box' by default and should be overridable via '-e server=<yourhost>'

## Contributing

If you would like to contribute to this project please read [How to contribute](CONTRIBUTING.md).

## License

This code is licensed under the [Apache License Version 2.0](LICENSE.md).
