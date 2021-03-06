#
# Revelation - a password manager for GNOME 2
# http://oss.codepoet.no/revelation/
# $Id$
#
# Module for handling plain text files
#
#
# Copyright (c) 2003-2006 Erik Grinaker
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from . import base
from revelation import entry

import time


class PlainText(base.DataHandler):
    "Data handler for plain text files"

    name        = "Plain text"
    importer    = False
    exporter    = True
    encryption  = False

    def export_data(self, entrystore, password = None):
        "Exports data to a plain text file"

        text = ""
        # fetch and sort entries
        iter = entrystore.iter_nth_child(None, 0)

        while iter is not None:
            e = entrystore.get_entry(iter)

            if type(e) == entry.FolderEntry:
                text += "%s [Folder]\n" % e.name
                text += "%s\n" % e.description
                text += "%s\n" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e.updated))
            else:
                text += "%s [%s]\n" % (e.name, e.typename)
                text += e.description != "" and "%s\n" % e.description or ""
                text += "%s\n" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e.updated))

                fields = [field for field in e.fields if field.value != ""]

                if len(fields) > 0:
                    text += "\n"
                    maxlen = max([len(field.name) for field in fields])

                    for field in fields:
                        text += "- " + field.name + ": " + (" " * (maxlen - len(field.name))) + field.value + "\n"

            text += "\n\n"

            iter = entrystore.iter_traverse_next(iter)

        return text
