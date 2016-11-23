from gbpautomation.heat.engine.resources import gbpresource
from heat.common.i18n import _
from heat.engine import properties
from neutronclient.common.exceptions import NeutronClientException
from heat.common import exception
from heat.engine import resource
from heat.engine import scheduler
from oslo_log import log as logging


LOG = logging.getLogger(__name__)


class ConfigureRadius(resource.Resource):

    PROPERTIES = (
        TENANT_ID, NAME, RULE
    ) = (
        'tenant_id', 'name', 'rule'
    )

    properties_schema = {
        TENANT_ID: properties.Schema(
            properties.Schema.STRING,
            _('Tenant id.')
        ),
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('Name of the radiues rule.'),
            update_allowed=True
        ),
        RULE: properties.Schema(
            properties.Schema.STRING,
            _('Radius rule.'),
            required=True,
            update_allowed=False
        )
    }

    def handle_create(self):
        import pdb; pdb.set_trace()
        result = self.properties.data[self.RULE].result()

        if result in ['poda']:
            LOG.info("XXXXXXX Successfully validated Radius Request.")
        self.resource_id_set(result)


def resource_mapping():
    return {
        'OS::Nfp::ConfigureRadius': ConfigureRadius}
