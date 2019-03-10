
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import jinja2
import json
import yaml
import os
from xossynchronizer.model_policies.policy import Policy

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))

class NextEPCMMEInstancePolicy(Policy):
    model_name = "NextEPCMMEInstance"

    def handle_create(self, service_instance):
        self.handle_update(service_instance)

    def handle_update(self, service_instance):
        owner = KubernetesService.objects.first()
        file = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "nextepc-mme.yaml")
        resource_definition = open(file).read()
        with open(file, 'r') as stream:
            try:
                print(yaml.load(stream))
            except yaml.YAMLError as exc:
                print(exc)

        name="nextepc-mme-%s" % service_instance.id
        instance = KubernetesResourceInstance(name=name, owner=owner, resource_definition=resource_definition, no_sync=False)

        instance.save()

    def handle_delete(self, service_instance):
        log.info("handle_delete")
        log.info("has a compute_instance")
        service_instance.compute_instance.delete()
        service_instance.compute_instance = None
        # TODO: I'm not sure we can save things that are being deleted...
        service_instance.save(update_fields=["compute_instance"])