# -*- coding: utf-8 -*-
import glob

import yaml
from guillotina import configure
from guillotina.i18n import MessageFactory


_ = MessageFactory("guillotina_cms")

app_settings = {
    "applications": [
        "guillotina.contrib.catalog.pg",
        "guillotina.contrib.swagger",
        "guillotina.contrib.dbusers",
    ],
    "available_blocks": {},
    "commands": {"create-container": "guillotina_cms.commands.create.CMSCreateCommand"},
    "load_utilities": {
        "guillotina_cms.workflow": {
            "provides": "guillotina_cms.interfaces.IWorkflowUtility",
            "factory": "guillotina_cms.utilities.workflow.WorkflowUtility",
            "settings": {},
        }
    },
    "layouts": {
        "CMSFolder": [
            "listing_view",
            "tabular_view",
            "summary_view",
            "layout_view",
            "full_view",
            "album_view",
            "event_listing",
            "document_view",
        ],
        "Document": ["document_view", "layout_view", "default"],
        "Container": ["document_view", "layout_view"],
        "News": ["document_view", "layout_view"],
        "Event": ["document_view", "layout_view"],
        "Link": ["document_view", "layout_view"],
        "File": ["document_view", "layout_view"],
        "Image": ["document_view", "layout_view"],
    },
    "workflows": {
        "private": {
            "initial_state": "private",
            "states": {"private": {"set_permission": {}, "actions": {}}},
        },
        "basic": {
            "initial_state": "private",
            "states": {
                "private": {
                    "actions": {
                        "publish": {
                            "title": "Publish",
                            "to": "public",
                            "check_permission": "guillotina.ReviewContent",
                        }
                    },
                    "set_permission": {
                        "roleperm": [
                            {
                                "setting": "Deny",
                                "role": "guillotina.Anonymous",
                                "permission": "guillotina.ViewContent",
                            },
                            {
                                "setting": "Deny",
                                "role": "guillotina.Anonymous",
                                "permission": "guillotina.AccessContent",
                            },
                        ]
                    },
                },
                "public": {
                    "actions": {
                        "retire": {
                            "title": "Retire",
                            "to": "private",
                            "check_permission": "guillotina.ReviewContent",
                        }
                    },
                    "set_permission": {
                        "roleperm": [
                            {
                                "setting": "AllowSingle",
                                "role": "guillotina.Anonymous",
                                "permission": "guillotina.ViewContent",
                            },
                            {
                                "setting": "AllowSingle",
                                "role": "guillotina.Anonymous",
                                "permission": "guillotina.AccessContent",
                            },
                        ]
                    },
                },
            },
        },
    },
    "workflows_content": {
        "guillotina.interfaces.IResource": "private",
        "guillotina.interfaces.IContainer": "basic",
        "guillotina_cms.content.document.IDocument": "basic",
        "guillotina_cms.content.image.IImage": "basic",
        "guillotina_cms.content.folder.IFolder": "basic",
    },
    "default_blocks": {
        "Document": {
            "blocks": {"tile1": {"@type": "title"}, "tile2": {"@type": "text"}},
            "blocks_layout": {"items": ["tile1", "tile2"]},
        },
        "Container": {
            "blocks": {"tile1": {"@type": "title"}, "tile2": {"@type": "text"}},
            "blocks_layout": {"items": ["tile1", "tile2"]},
        },
    },
    "global_disallowed_types": [
        "User",
        "UserManager",
        "Group",
        "GroupManager",
        "Item",
        "Container",
        "Folder",
    ],
    "default_allow_discussion": False,
    "allow_discussion_types": [],
    "store_json": True,
}

path = "/".join(__file__.split("/")[:-1])

for workflow_file in glob.glob(path + "/workflows/*.yaml"):
    with open(workflow_file, "r") as f:
        workflow_content = yaml.load(f, Loader=yaml.FullLoader)
    ident = workflow_file.split("/")[-1].rstrip(".yaml")
    app_settings["workflows"][ident] = workflow_content


def includeme(root, settings):
    configure.scan("guillotina_cms.interfaces")
    configure.scan("guillotina_cms.api")
    configure.scan("guillotina_cms.behaviors")
    configure.scan("guillotina_cms.content")
    configure.scan("guillotina_cms.fields")
    configure.scan("guillotina_cms.json")
    configure.scan("guillotina_cms.utilities")
    configure.scan("guillotina_cms.vocabularies")
    configure.scan("guillotina_cms.permissions")
    configure.scan("guillotina_cms.install")
    configure.scan("guillotina_cms.subscribers")
    configure.scan("guillotina_cms.blocks")

    if "guillotina_elasticsearch" in settings.get("applications", []):
        if "load_utilities" not in settings:
            settings["load_utilities"] = {}
        from guillotina.contrib.catalog.pg import app_settings as pg_app_settings

        settings["load_utilities"]["pg_catalog"] = {
            **pg_app_settings["load_utilities"]["catalog"],
            **{"name": "pg_catalog"},
        }
