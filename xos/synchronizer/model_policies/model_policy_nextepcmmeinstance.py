import base64
import jinja2
import json
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.policy import Policy

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))


class NextEPCMMEInstancePolicy(Policy):
    model_name = "NextEPCMMEInstance"

    def handle_create(self, service_instance):
        return self.handle_update(service_instance)

    def handle_update(self, service_instance):
        owner = KubernetesService.objects.first()
        template = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "nextepc-mme.yaml")
        f = open(template).read()

        resource_definition = f.read()
        name="nextepc-mme-%s" % service_instance.id
        instance = KubernetesResourceInstance(name=name, owner=owner, resource_definition=resource_definition,no_sync=False)

        instance.save()

    def handle_delete(self, service_instance):
        log.info("handle_delete")
        log.info("has a compute_instance")
        service_instance.compute_instance.delete()
        service_instance.compute_instance = None
        # TODO: I'm not sure we can save things that are being deleted...
        service_instance.save(update_fields=["compute_instance"])