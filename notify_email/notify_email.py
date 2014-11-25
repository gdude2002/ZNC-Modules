__author__ = 'Gareth Coles'

import mako
import os
import requests
import yaml

import znc


DEFAULT_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>Highlighted on IRC</title>
</head>
<body>
    <h1>Highlighted on IRC</h1>

    <p>This is a notification and some context for your highlight on "${network}".</p>

    <pre>
% for pre in pre_messages:
    [${pre.time | h}] &lt;${pre.user | h}&gt; ${pre.text | h}
% endfor
 >> [${message.time | h}] &lt;${message.user | h}&gt; ${message.text | h}
% for post in post_messages:
    [${post.time | h}] &lt;${post.user | h}&gt; ${post.text | h}
% endfor
    </pre>
</body>
</html>
"""


DEFAULT_PLAIN_TEMPLATE = """Highlighted on IRC
==================

This is a notification and some context for your highlight on "${network}".

% for pre in pre_messages:
    [${pre.time}] <${pre.user}> ${pre.text}
% endfor
 >> [${message.time}] <${message.user}> ${message.text}
% for post in post_messages:
    [${post.time}] <${post.user}> ${post.text}
% endfor
"""


class notify_email(znc.Module):
    description = "Sends an email when highlighted, if not attached."
    module_types = [znc.CModInfo.NetworkModule]

    config = {}

    html_template = ""
    plain_template = ""

    path = ""

    def OnLoad(self, sArgsi, sMessage):
        self.path = self.GetNetwork().GetNetworkPath() + "/moddata/notify_email/"

        if not os.path.isdir(self.path):
            os.mkdir(self.path)

        if not os.path.exists(self.path + "template.html"):
            fh = open(self.path + "template.html", "w")
            fh.write(DEFAULT_HTML_TEMPLATE)
            fh.flush()
            fh.close()

        if not os.path.exists(self.path + "template.txt"):
            fh = open(self.path + "template.txt", "w")
            fh.write(DEFAULT_PLAIN_TEMPLATE)
            fh.flush()
            fh.close()

        if not os.path.exists(self.path + "config.yml"):
            fh = open(self.path + "config.yml", "w")
            fh.flush()
            fh.close()

        self.load_config()

        if self.config is None:
            # TODO: defaults
            pass

        fh = open(self.path + "template.html", "r")
        self.html_template = fh.read()
        fh.close()

        fh = open(self.path + "template.txt", "r")
        self.plain_template = fh.read()
        fh.close()

        return znc.CONTINUE

    def load_config(self):
        fh = open(self.path + "config.yml", "r")
        self.config = yaml.load(fh)
        fh.close()

    def save_config(self):
        fh = open(self.path + "config.yml", "w")
        fh.write(yaml.dump(self.config))
        fh.flush()
        fh.close()

    def OnModCommand(self, sCommand):
        self.PutModule("Path: {0}".format(self.path))
        
        if self.GetUser().IsUserAttached():
            self.PutModule("It appears that you are attached!")
        else:
            self.PutModule("Apparently, you're not attached.")
        return znc.CONTINUE
