import base64
import jinja2
import json
import yaml
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.policy import Policy

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))


class NextEPCServiceInstancePolicy(Policy):
    model_name = "NextEPCServiceInstance"

    def handle_create(self, service_instance):
        log.info("handle_create NextEPCServiceInstance")
        return self.handle_update(service_instance)

    def handle_update(self, service_instance):
        log.info("handle_update NextEPCServiceInstance")
        owner = KubernetesService.objects.first()
        type = service_instance.type.lower()
        file = "nextepc-" + type + ".yaml"
        input_file = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))),
                                  file)
        with open(input_file, 'r') as stream:
            try:
                resource_definition = json.dumps(yaml.load(stream), sort_keys=True, indent=2)
                stream.close()
            except yaml.YAMLError as exc:
                resource_definition = "{}"
                print(exc)

        name = "nextepc-" + + "%s" % service_instance.id
        instance = KubernetesResourceInstance(name=name, owner=owner,
                                              resource_definition=resource_definition,
                                              no_sync=False)

        instance.save()

    def handle_delete(self, service_instance):
        log.info("handle_delete NextEPCServiceInstance")
        service_instance.compute_instance.delete()
        service_instance.compute_instance = None
        service_instance.save(update_fields=["compute_instance"])
