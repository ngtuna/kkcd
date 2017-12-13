#!/usr/bin/env python
"""A controller """

from kubernetes import client, config, watch
import logging

class Ingress(object):
    def __init__(self, obj):
        self._obj = obj
        self._apiversion = obj.api_version
        self._kind = obj.kind
        self._metadata = obj.metadata
        self._spec = obj.spec

    def ing_name(self):
        return self._metadata.name

def main():
    # config.load_incluster_config()
    config.load_kube_config()

    ext_beta1 = client.ExtensionsV1beta1Api()

    def process_meta(t, ing):
        if t == "DELETED":
            logging.warning("ingress %s has been deleted", ing.ing_name())
            # process_delete(ing)
        elif t == "MODIFIED":
            logging.warning("ingress %s has been updated", ing.ing_name())
            # process_update(ing)
        elif t == "ADDED":
            logging.warning("ingress %s has been created", ing.ing_name())
            # process_add(ing)
        else:
            logging.error("Unrecognized type: %s", t)

    resource_version = ""
    while True:
        stream = watch.Watch().stream(ext_beta1.list_ingress_for_all_namespaces,
                                      resource_version=resource_version)
        for event in stream:
            try:
                t = event["type"]
                obj = event["object"]
                print obj
                ing = Ingress(obj)
                process_meta(t, ing)

                # Configure where to resume streaming.
                metadata = obj.metadata
                if metadata:
                    resource_version = metadata.resource_version
            except:
                logging.exception("Error handling event")

if __name__ == "__main__":
    main()
