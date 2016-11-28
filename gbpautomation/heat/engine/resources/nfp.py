from heat.common.i18n import _
from heat.engine import properties
from heat.common import exception
from heat.engine import resource
from heat.engine import scheduler
from oslo_log import log as logging
import radius_driver as r_dvr
import json
import time
import struct

LOG = logging.getLogger(__name__)


class CheckDeviceUp(resource.Resource):

    PROPERTIES = (MGMT_IP) = ('mgmt_ip')

    properties_schema = {
        MGMT_IP: properties.Schema(
            properties.Schema.STRING,
            _('Service Management IP of the device.'))}

    def handle_create(self):
        time.sleep(10)
        mgmt_ip = self.properties.data['mgmt_ip'].result()
        LOG.info("XXX Device at %s is UP." % mgmt_ip)
        self.resource_id_set('device_up')


class ConfigureDevice(resource.Resource):

    PROPERTIES = (
        TENANT_ID, NAME, DATA
    ) = (
        'tenant_id', 'name', 'data'
    )

    properties_schema = {
        TENANT_ID: properties.Schema(
            properties.Schema.STRING,
            _('Tenant id.')
        ),
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('Name of the radius rule.'),
            update_allowed=True
        ),
        DATA: properties.Schema(
            properties.Schema.STRING,
            _('Radius rules.'),
            required=True,
            update_allowed=False
        )
    }

    def get_client(self):
        return r_dvr.RadiusDriver()

    def validate_and_retrieve_data(self, properties):
        req_attr = ['user_name', 'password', 'host_ip', 'dbms_name']
        data = json.loads(properties['data'].result())
        if set(req_attr) == set(data):
            return data
        raise Exception("Schema validation failed")

    def handle_create(self):
        data = self.validate_and_retrieve_data(self.properties.data)
        data = json.dumps(data)
        LOG.info("XXX Data %s is validated." % data)
        client = self.get_client()

        client.configure_radius(data)
        LOG.info("XXX Device is configured.")

        self.resource_id_set('device_configured')


def resource_mapping():
    return {
        'OS::Nfp::ConfigureDevice': ConfigureDevice,
        'OS::Nfp::CheckDeviceUp': CheckDeviceUp}
