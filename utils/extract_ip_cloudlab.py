import re

def extract_host_info(xml_content):
    pattern = re.compile(r'<host name="(.+?)" ipv4="(.+?)"/>')
    matches = pattern.findall(xml_content)
    
    host_info = []
    for match in matches:
        hostname = match[0]
        ip_address = match[1]
        host_info.append(f"{ip_address} {hostname}")
    
    return host_info

# Example XML content
xml_content = '''
<rspec xmlns="http://www.geni.net/resources/rspec/3" xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" xmlns:tour="http://www.protogeni.net/resources/rspec/ext/apt-tour/1" xmlns:jacks="http://www.protogeni.net/resources/rspec/ext/jacks/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.geni.net/resources/rspec/3    http://www.geni.net/resources/rspec/3/request.xsd" type="request">
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="nfs" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc836" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701274">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="nfs:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc836:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701298" mac_address="0257519c3c19">
      <ip address="10.10.1.1" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <interface client_id="nfs:if1" component_id="urn:publicid:IDN+emulab.net+interface+pc836:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701341" mac_address="02bdfa22baf2">
      <ip address="10.254.254.254" type="ipv4" netmask="255.255.255.252"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc836.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-server.sh"/>
    </services>
    <emulab:vnode name="pc836" hardware_type="d430"/>
    <host name="nfs.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.136"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="dsnode" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+dbox2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701265" exclusive="false">
    <sliver_type name="emulab-blockstore"/>
    <interface client_id="dsnode:if0" component_id="urn:publicid:IDN+emulab.net+interface+dbox2:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701340" mac_address="0221bd7b1683">
      <ip address="10.254.254.253" type="ipv4" netmask="255.255.255.252"/>
    </interface>
    <emulab:blockstore name="dsnode-bs" class="remote" placement="any" readonly="true"/>
    <emulab:vnode name="dboxvm2-1" hardware_type="blockstore"/>
    <host name="dsnode.Exp-n40.CloudProf.emulab.net"/>
    <services>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="probirr"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="whitspen"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="akazad"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="lmenard"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="anupbh"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="alibusta"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="nishita"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="nishitad"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="manishn"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="Pravali"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="vrundak"/>
      <login authentication="ssh-keys" hostname="dbox2.emulab.net" port="29042" username="ppaiva"/>
      <emulab:console server="dbox2.emulab.net"/>
      <emulab:imageable available="true"/>
    </services>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node1" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc427" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701289">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node1:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc427:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701299" mac_address="02e7457e100f">
      <ip address="10.10.1.2" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc427.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc427" hardware_type="d710"/>
    <host name="node1.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.27"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node2" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc402" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701291">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node2:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc402:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701300" mac_address="0239e2fd3aa8">
      <ip address="10.10.1.3" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc402.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc402" hardware_type="d710"/>
    <host name="node2.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.2"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node3" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc762" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701295">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node3:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc762:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701301" mac_address="026e72a163b3">
      <ip address="10.10.1.4" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc762.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc762" hardware_type="d430"/>
    <host name="node3.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.62"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node4" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc443" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701292">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node4:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc443:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701302" mac_address="02e08f663a6f">
      <ip address="10.10.1.5" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc443.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv6.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc443" hardware_type="d710"/>
    <host name="node4.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.43"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node5" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc518" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701257">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node5:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc518:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701303" mac_address="02e837b96cf4">
      <ip address="10.10.1.6" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc518.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc518" hardware_type="d710"/>
    <host name="node5.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.118"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node6" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc797" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701269">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node6:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc797:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701304" mac_address="021e94d211af">
      <ip address="10.10.1.7" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc797.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc797" hardware_type="d430"/>
    <host name="node6.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.97"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node7" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc552" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701268">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node7:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc552:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701305" mac_address="020959586fd7">
      <ip address="10.10.1.8" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc552.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc552" hardware_type="d710"/>
    <host name="node7.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.152"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node8" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc740" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701261">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node8:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc740:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701306" mac_address="02c5b6dc0a95">
      <ip address="10.10.1.9" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc740.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc740" hardware_type="d430"/>
    <host name="node8.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.40"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node9" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc791" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701293">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node9:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc791:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701307" mac_address="024be63c822c">
      <ip address="10.10.1.10" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc791.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc791" hardware_type="d430"/>
    <host name="node9.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.91"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node10" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc403" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701254">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node10:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc403:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701308" mac_address="0251e3dd56ca">
      <ip address="10.10.1.11" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc403.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc403" hardware_type="d710"/>
    <host name="node10.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.3"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node11" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc434" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701277">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node11:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc434:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701309" mac_address="02109f6c32f0">
      <ip address="10.10.1.12" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc434.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc434" hardware_type="d710"/>
    <host name="node11.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.34"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node12" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc419" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701282">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node12:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc419:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701310" mac_address="02bc7568c04e">
      <ip address="10.10.1.13" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc419.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv6.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc419" hardware_type="d710"/>
    <host name="node12.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.19"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node13" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc442" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701255">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node13:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc442:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701311" mac_address="026858eaaafd">
      <ip address="10.10.1.14" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc442.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc442" hardware_type="d710"/>
    <host name="node13.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.42"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node14" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc778" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701280">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node14:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc778:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701312" mac_address="02e764e80d00">
      <ip address="10.10.1.15" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc778.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc778" hardware_type="d430"/>
    <host name="node14.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.78"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node15" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc814" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701281">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node15:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc814:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701313" mac_address="02cb8d47f05a">
      <ip address="10.10.1.16" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc814.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc814" hardware_type="d430"/>
    <host name="node15.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.114"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node16" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc520" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701258">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node16:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc520:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701314" mac_address="02d14c96e294">
      <ip address="10.10.1.17" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc520.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc520" hardware_type="d710"/>
    <host name="node16.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.120"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node17" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc544" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701275">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node17:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc544:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701315" mac_address="02ec01333ecf">
      <ip address="10.10.1.18" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc544.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc544" hardware_type="d710"/>
    <host name="node17.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.144"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node18" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc831" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701290">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node18:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc831:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701316" mac_address="02af35fb6399">
      <ip address="10.10.1.19" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc831.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc831" hardware_type="d430"/>
    <host name="node18.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.131"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node19" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc497" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701267">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node19:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc497:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701317" mac_address="02aab0047a0e">
      <ip address="10.10.1.20" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc497.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc497" hardware_type="d710"/>
    <host name="node19.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.97"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node20" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc506" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701262">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node20:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc506:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701318" mac_address="02f9f7a50722">
      <ip address="10.10.1.21" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc506.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc506" hardware_type="d710"/>
    <host name="node20.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.106"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node21" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc729" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701259">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node21:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc729:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701319" mac_address="023e15fbbb3c">
      <ip address="10.10.1.22" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc729.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc729" hardware_type="d430"/>
    <host name="node21.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.29"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node22" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc491" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701286">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node22:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc491:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701320" mac_address="025fd5c809cc">
      <ip address="10.10.1.23" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc491.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc491" hardware_type="d710"/>
    <host name="node22.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.91"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node23" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc426" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701287">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node23:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc426:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701321" mac_address="024acaa0b19c">
      <ip address="10.10.1.24" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc426.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc426" hardware_type="d710"/>
    <host name="node23.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.26"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node24" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc510" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701278">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node24:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc510:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701322" mac_address="02aa698f494c">
      <ip address="10.10.1.25" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc510.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc510" hardware_type="d710"/>
    <host name="node24.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.110"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node25" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc724" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701264">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node25:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc724:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701323" mac_address="02d86d80ceb1">
      <ip address="10.10.1.26" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc724.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc724" hardware_type="d430"/>
    <host name="node25.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.24"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node26" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc722" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701279">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node26:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc722:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701324" mac_address="02c2abe44375">
      <ip address="10.10.1.27" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc722.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc722" hardware_type="d430"/>
    <host name="node26.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.22"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node27" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc721" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701273">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node27:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc721:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701325" mac_address="02a82a145768">
      <ip address="10.10.1.28" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc721.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc721" hardware_type="d430"/>
    <host name="node27.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.21"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node28" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc431" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701283">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node28:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc431:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701326" mac_address="026c4b91404b">
      <ip address="10.10.1.29" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc431.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc431" hardware_type="d710"/>
    <host name="node28.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.31"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node29" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc738" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701294">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node29:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc738:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701327" mac_address="0271c892a725">
      <ip address="10.10.1.30" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc738.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc738" hardware_type="d430"/>
    <host name="node29.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.38"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node30" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc513" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701270">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node30:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc513:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701328" mac_address="02236e805bef">
      <ip address="10.10.1.31" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc513.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc513" hardware_type="d710"/>
    <host name="node30.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.113"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node31" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc509" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701285">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node31:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc509:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701329" mac_address="02024a460477">
      <ip address="10.10.1.32" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc509.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc509" hardware_type="d710"/>
    <host name="node31.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.109"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node32" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc404" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701263">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node32:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc404:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701330" mac_address="025fd13870fd">
      <ip address="10.10.1.33" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc404.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc404" hardware_type="d710"/>
    <host name="node32.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.4"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node33" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc731" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701276">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node33:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc731:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701331" mac_address="02d7c4f86ab7">
      <ip address="10.10.1.34" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc731.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc731" hardware_type="d430"/>
    <host name="node33.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.31"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node34" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc412" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701260">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node34:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc412:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701332" mac_address="02a6254a6fbd">
      <ip address="10.10.1.35" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc412.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv6.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc412" hardware_type="d710"/>
    <host name="node34.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.12"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node35" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc415" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701256">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node35:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc415:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701333" mac_address="02bf6773a18b">
      <ip address="10.10.1.36" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc415.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv6.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc415" hardware_type="d710"/>
    <host name="node35.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.15"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node36" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc435" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701271">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node36:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc435:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701334" mac_address="0238e8ae28cc">
      <ip address="10.10.1.37" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc435.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc435" hardware_type="d710"/>
    <host name="node36.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.35"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node37" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc416" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701266">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node37:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc416:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701335" mac_address="02bd9272c45c">
      <ip address="10.10.1.38" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc416.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv6.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc416" hardware_type="d710"/>
    <host name="node37.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.16"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node38" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc433" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701284">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node38:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc433:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701336" mac_address="028eb9bef4dc">
      <ip address="10.10.1.39" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc433.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="tipserv5.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc433" hardware_type="d710"/>
    <host name="node38.Exp-n40.CloudProf.emulab.net" ipv4="155.98.38.33"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node39" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc723" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701272">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node39:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc723:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701337" mac_address="02adf9ddefcf">
      <ip address="10.10.1.40" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc723.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc723" hardware_type="d430"/>
    <host name="node39.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.23"/>
  </node>
  <node xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="node40" exclusive="true" component_manager_id="urn:publicid:IDN+emulab.net+authority+cm" component_id="urn:publicid:IDN+emulab.net+node+pc834" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701288">
    <sliver_type name="raw-pc">
      <disk_image name="urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"/>
    </sliver_type>
    <interface client_id="node40:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc834:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701338" mac_address="02d3fccc7907">
      <ip address="10.10.1.41" type="ipv4" netmask="255.255.255.0"/>
    </interface>
    <services>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="probirr"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="whitspen"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="arjunsh"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="ssmtariq"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="akazad"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="lmenard"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="wilkowsk"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="SonjoyKP"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="sonjoyp"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="eejoylim"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="Shreyba"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="anupbh"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="alibusta"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="nishita"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="nishitad"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="manishn"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="Pravali"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="lkolluru"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="vrundak"/>
      <login authentication="ssh-keys" hostname="pc834.emulab.net" port="22" username="ppaiva"/>
      <emulab:console server="boss.emulab.net"/>
      <emulab:recovery available="true"/>
      <emulab:powercycle available="true"/>
      <emulab:imageable available="true"/>
      <execute shell="sh" command="sudo /bin/bash /local/repository/nfs-client.sh"/>
    </services>
    <emulab:vnode name="pc834" hardware_type="d430"/>
    <host name="node40.Exp-n40.CloudProf.emulab.net" ipv4="155.98.36.134"/>
  </node>
  <link xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="nfsLan" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701297" vlantag="212">
    <interface_ref client_id="nfs:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc836:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701298"/>
    <interface_ref client_id="node1:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc427:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701299"/>
    <interface_ref client_id="node2:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc402:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701300"/>
    <interface_ref client_id="node3:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc762:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701301"/>
    <interface_ref client_id="node4:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc443:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701302"/>
    <interface_ref client_id="node5:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc518:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701303"/>
    <interface_ref client_id="node6:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc797:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701304"/>
    <interface_ref client_id="node7:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc552:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701305"/>
    <interface_ref client_id="node8:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc740:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701306"/>
    <interface_ref client_id="node9:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc791:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701307"/>
    <interface_ref client_id="node10:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc403:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701308"/>
    <interface_ref client_id="node11:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc434:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701309"/>
    <interface_ref client_id="node12:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc419:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701310"/>
    <interface_ref client_id="node13:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc442:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701311"/>
    <interface_ref client_id="node14:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc778:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701312"/>
    <interface_ref client_id="node15:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc814:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701313"/>
    <interface_ref client_id="node16:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc520:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701314"/>
    <interface_ref client_id="node17:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc544:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701315"/>
    <interface_ref client_id="node18:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc831:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701316"/>
    <interface_ref client_id="node19:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc497:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701317"/>
    <interface_ref client_id="node20:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc506:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701318"/>
    <interface_ref client_id="node21:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc729:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701319"/>
    <interface_ref client_id="node22:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc491:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701320"/>
    <interface_ref client_id="node23:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc426:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701321"/>
    <interface_ref client_id="node24:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc510:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701322"/>
    <interface_ref client_id="node25:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc724:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701323"/>
    <interface_ref client_id="node26:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc722:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701324"/>
    <interface_ref client_id="node27:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc721:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701325"/>
    <interface_ref client_id="node28:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc431:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701326"/>
    <interface_ref client_id="node29:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc738:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701327"/>
    <interface_ref client_id="node30:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc513:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701328"/>
    <interface_ref client_id="node31:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc509:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701329"/>
    <interface_ref client_id="node32:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc404:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701330"/>
    <interface_ref client_id="node33:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc731:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701331"/>
    <interface_ref client_id="node34:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc412:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701332"/>
    <interface_ref client_id="node35:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc415:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701333"/>
    <interface_ref client_id="node36:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc435:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701334"/>
    <interface_ref client_id="node37:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc416:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701335"/>
    <interface_ref client_id="node38:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc433:eth4" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701336"/>
    <interface_ref client_id="node39:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc723:eth1" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701337"/>
    <interface_ref client_id="node40:if0" component_id="urn:publicid:IDN+emulab.net+interface+pc834:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701338"/>
    <link_type name="lan"/>
    <emulab:vlan_tagging enabled="true"/>
    <emulab:best_effort enabled="true"/>
    <emulab:link_multiplexing enabled="true"/>
    <component_manager name="urn:publicid:IDN+emulab.net+authority+cm"/>
    <emulab:switchpath>procurve1:procurve5 procurve1:procurve3 procurve1:z9500 procurve1:procurve4</emulab:switchpath>
  </link>
  <link xmlns:emulab="http://www.protogeni.net/resources/rspec/ext/emulab/1" client_id="dslink" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701339" vlantag="213">
    <interface_ref client_id="dsnode:if0" component_id="urn:publicid:IDN+emulab.net+interface+dbox2:eth2" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701340"/>
    <interface_ref client_id="nfs:if1" component_id="urn:publicid:IDN+emulab.net+interface+pc836:eth3" sliver_id="urn:publicid:IDN+emulab.net+sliver+1701341"/>
    <emulab:vlan_tagging enabled="true"/>
    <emulab:best_effort enabled="true"/>
    <emulab:link_multiplexing enabled="true"/>
    <component_manager name="urn:publicid:IDN+emulab.net+authority+cm"/>
  </link>
  <rspec_tour xmlns="http://www.protogeni.net/resources/rspec/ext/apt-tour/1">
    <description type="markdown">This profile sets up a simple NFS server and a network of clients. The NFS server uses
a long term dataset that is persistent across experiments. In order to use this profile,
you will need to create your own dataset and use that instead of the demonstration 
dataset below. If you do not need persistant storage, we have another profile that
uses temporary storage (removed when your experiment ends) that you can use. </description>
    <instructions type="markdown">Click on any node in the topology and choose the `shell` menu item. Your shared NFS directory is mounted at `/nfs` on all nodes.</instructions>
  </rspec_tour>
  <data_set xmlns="http://www.protogeni.net/resources/rspec/ext/profile-parameters/1">
    <data_item name="emulab.net.parameter.linkSpeed">10000000</data_item>
    <data_item name="emulab.net.parameter.tempFileSystemMax">True</data_item>
    <data_item name="emulab.net.parameter.bestEffort">True</data_item>
    <data_item name="emulab.net.parameter.phystype">d710</data_item>
    <data_item name="emulab.net.parameter.osImage">urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD</data_item>
    <data_item name="emulab.net.parameter.clientCount">40</data_item>
  </data_set>
  <emulab:portal name="cloudlab" url="https://www.cloudlab.us/status.php?uuid=e70f5c74-91f3-11f0-bc80-e4434b2381fc" project="CloudProf" experiment="Exp-n40" sequence="1757913725"/>
  <rs:site_info xmlns:rs="http://www.protogeni.net/resources/rspec/ext/site-info/1">
    <rs:location country="US" latitude="40.768652" longitude="-111.84581"/>
  </rs:site_info>
</rspec>
'''

# Extract host information
host_info = extract_host_info(xml_content)

# Write the extracted information to a file
with open("host_info.txt", "w") as file:
    for entry in host_info:
        file.write(entry + "\n")

print("Host information extracted and saved to host_info.txt")