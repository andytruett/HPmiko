# import hpmiko.templates
import tempfile
import textfsm
import netmiko
from . import templates

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources


class HP:
    def __init__(self, ip: str, username: str, password: str):
        self.ip = ip
        self.password = password
        self.username = username

    def connect(self, port=22, verbosity=False):
        """Establish SSH connection to the access point

        Parameters
        ----------
        verbosity : bool, optional
            Toggle verbose SSH connection information, by default False
        """

        switch = {
            "device_type": "hp_procurve",
            "ip": self.ip,
            "username": self.username,
            "password": self.password,
            "port": port,
            "verbose": verbosity,
        }

        self.net_connect = netmiko.ConnectHandler(**switch)
        self.net_connect.find_prompt()

    def disconnect(self):
        return self.net_connect.disconnect()

    def send_command(self, command: str):
        """Send CLI command to switch and return raw response

        Parameters
        ----------
        command : str
            CLI command to send

        Returns
        -------
        str
            raw CLI response
        """
        return self.net_connect.send_command(command)

    def send_config(self, command_list: list):
        """Send list of CLI commands to access point

        Parameters
        ----------
        command_list : list
            list of CLI commands to send to switch

        Returns
        -------
        str
            CLI output resulting from switch
        """
        return self.net_connect.send_config_set(command_list)

    def fsm_parse(self, command_response: str, template=str):
        """Get structured data from CLI command response, via textFSM template

        Parameters
        ----------
        command : str
            response string from CLI
        template : str
            raw textFSM template string
            or
            name of predefined template from aeromiko package
        raw : boolean

        Returns
        -------
        dict
            structured data extracted from CLI response
        """
        if template.startswith("Value"):
            textfsm_template = template
        else:
            textfsm_template = pkg_resources.read_text(templates, template)

        tmp = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp.name, "w") as file:
            file.write(textfsm_template)
        with open(tmp.name, "r") as file:
            fsm = textfsm.TextFSM(file)
            fsm_results = fsm.ParseText(command_response)
            info = [dict(zip(fsm.header, row)) for row in fsm_results]
        for information in info:
            for (key, value) in information.items():
                information[key] = value.strip()
        return info

    # def show_config_running(self):
    #     pass

    def get_hostname(self):
        """Get hostname from `show system`

        Returns
        -------
        str
            Switch hostname
        """
        command = "show system"
        template = "show_system.textfsm"

        command_response = self.send_command(command)
        hostname_info = self.fsm_parse(command_response, template)
        hostname = hostname_info[0]["NAME"]

        return hostname

    def show_system(self):
        """Show system

        Returns
        -------
        dict
            NAME
            CONTACT
            LOCATION
            MAC_AGE
            TIMEZONE
            DAYLIGHT_RULE
            SOFTWARE_VERSION
            ROM_VERSION
            ALLOW_MODS
            MAC
            SERIAL
            UPTIME
            CPU_UTIL
            MEM_TOT
            MEM_FREE
            PACKETS_RX
            PACKETS_TX
            PACKETS_TOT
            BUFFERS_FREE
            BUFFERS_LOWEST
            BUFFERS_MISSED
        """
        command = "show system"
        template = "show_system.textfsm"

        command_response = self.send_command(command)
        system_info = self.fsm_parse(command_response, template)

        return system_info

    def show_vlan(self, vlan: str):
        vlan = str(vlan)

        command = "show vlan " + vlan
        template = "show_vlan.textfsm"

        command_response = self.send_command(command)
        vlan_info = self.fsm_parse(command_response, template)

        return vlan_info

    def show_vlans(self):
        command = "show vlans"
        template = "show_vlans.textfsm"

        command_response = self.send_command(command)
        vlans_info = self.fsm_parse(command_response, template)

        return vlans_info

    def show_name(self):
        command = "show name"
        template = "show_name.textfsm"

        command_response = self.send_command(command)
        name_info = self.fsm_parse(command_response, template)

        return name_info

    def get_interfaces(self):
        command = "sh int status"
        template = "get_interfaces.textfsm"

        command_response = self.send_command(command)
        interfaces_info = self.fsm_parse(command_response, template)

        return interfaces_info

    def show_lldp_in_re(self):
        command = "show lldp in re"
        template = "show_lldp_info_re.textfsm"

        command_response = self.send_command(command)
        lldp_info = self.fsm_parse(command_response, template)

        return lldp_info

    def show_lldp_in_re_detail(self, port: str):
        port = str(port)
        command = "show lldp in re " + port

        template = "show_lldp_info_re_int.textfsm"
        command_response = self.send_command(command)
        port_lldp_info = self.fsm_parse(command_response, template)

        return port_lldp_info

    def show_int_transceiver_detail(self, port: str):
        port = str(port)

        command = "show int transceiver" + port
        template = "show_int_transceiver_detail.textfsm"

        command_response = self.send_command(command)
        transceiver_info = self.fsm_parse(command_response, template)

        return transceiver_info

    def show_tech_buffers(self):
        command = "show tech buffer"
        template = "show_tech_buffers.textfsm"

        command_response = self.send_command(command)
        tech_info = self.fsm_parse(command_response, template)

        return tech_info
