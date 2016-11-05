# Copyright 2016 Ivan Kukharchuk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Groovy label selection plugin integration

"""


import logging
import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base
import pkg_resources

logger = logging.getLogger(__name__)
GROOVY_PLUGIN_CLASS_NAME='jp.ikedam.jenkins.plugins.groovy__label__assignment.GroovyLabelAssignmentProperty'

class GroovyLabelAssignment(jenkins_jobs.modules.base.Base):
    sequence = 81

    component_type = 'groovy-label'
    component_list_type = 'groovy-labels'


    def gen_xml(self, xml_parent, data):
        groovy_plugin_info = self.registry.get_plugin_info("Groovy Label Assignment plugin")
        groovy_plugin_version = pkg_resources.parse_version(groovy_plugin_info.get('version', '0'))
        security_plugin_info = self.registry.get_plugin_info("Script Security Plugin")
        security_plugin_version = pkg_resources.parse_version(security_plugin_info.get('version', '0'))
        groovy_script = data.get('groovy-label-script', False)
        groovy_sandbox = data.get('groovy-label-sandbox', False)
        if groovy_script:
            properties_elem = xml_parent.find('properties')
            if properties_elem is None:
                properties_elem = XML.SubElement(xml_parent, 'properties')

            groovy_script_elem = XML.SubElement(properties_elem, GROOVY_PLUGIN_CLASS_NAME)
            groovy_script_elem.set('plugin', "groovy-label-assignment@%s" % groovy_plugin_version)

            secure_script_elem = XML.SubElement(groovy_script_elem, 'secureGroovyScript')
            secure_script_elem.set('plugin', "script-security@%s" % security_plugin_version)
            XML.SubElement(secure_script_elem, 'script').text = groovy_script
            XML.SubElement(secure_script_elem, 'sandbox').text = str(groovy_sandbox).lower()
