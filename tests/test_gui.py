import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject
from os import walk
import threading
import time
from executable import Executable
from stats import StatsControl

import xml.etree.cElementTree as et

class Handler:

    indexation_parameters = {
        "has_stemming": False,
        "has_stop_words_removal": False,
        "has_compression": False,
        "files_list": []
    }

    query_parameters = {
        "algorithm": "NAIVE",
        "results_number": 5,
        "query": ""
    }

    state = {
        "indexation_done": False,
        "query_complete": False
    }

    backend = Executable()

    @staticmethod
    def get_filelist_from_folderpath(folderpath):
        filenameslist = []

        # Get all file names in folder at first level only
        for (dirpath, dirnames, filenames) in walk(folderpath):
            filenameslist.extend(filenames)
            break

        # Concatenate them with folder path
        filelist = [folderpath + "/" + filename for filename in filenameslist]

        return filelist

    def get_document_from_DOCID_and_filepath(docid, filepath):
        documentViews = []

        with open(filepath) as file:
            document_string = ""
            for line in file:
                document_string = "{}\n{}".format(document_string, line)
                if "</DOC>" in line:
                    documentView = et.fromstring(document_string)

                    for el in documentView.findall('DOC'):
                        print('-------------------')
                        for ch in el.getchildren():
                            print('{:>15}: {:<30}'.format(ch.tag, ch.text))

                    documentViews.append(documentView)
                    document_string = ""

        #TODO here get the right document by ID

        return document

    def toggle_stemming(self, button):
        print("Toggle stemming to " + str(button.get_active()))
        self.indexation_parameters["has_stemming"] = button.get_active()

    def toggle_stop_words_removal(self, button):
        print("Toggle stop words removal to " + str(button.get_active()))
        self.indexation_parameters["has_stop_words_removal"] = button.get_active()

    def toggle_compression(self, button):
        print("Toggle compression to " + str(button.get_active()))
        self.indexation_parameters["has_compression"] = button.get_active()

    def open_file_chooser(self, button):
        print("Open file chooser")
        main_window = builder.get_object("main_window")
        dialog = Gtk.FileChooserDialog("Please choose a folder", main_window,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            folder_path = dialog.get_filename()
            print("Select clicked")
            print("Folder selected: " + folder_path)
            choose_folder_label = builder.get_object("choose_folder_label")
            choose_folder_label.set_text(folder_path);

            # Get all files in that folder
            self.indexation_parameters["files_list"] = self.get_filelist_from_folderpath(folder_path)
            print(self.indexation_parameters["files_list"])

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def start_indexation(self, button):
        print("Start indexation")

        loading_box = builder.get_object("loading_box")
        loading_box.set_visible(True)

        query_box = builder.get_object("query_box")
        results_box = builder.get_object("results_box")
        query_box.set_visible(False)
        results_box.set_visible(False)

        self.backend.indexing(files=self.indexation_parameters["files_list"],
                              ignore_stop_words=self.indexation_parameters["has_stop_words_removal"],
                              stemming=self.indexation_parameters["has_stemming"],
                              use_vbytes=self.indexation_parameters["has_compression"]
                              #ignore_case=self.indexation_parameters[""],
                              #date_weight=
                              #title_weight=
                              #use_weights=
                              #memory_limit=
                                )
        # # Reset this state variable
        # self.state["indexation_done"] = False
        #
        # loading_box = builder.get_object("loading_box")
        # loading_box.set_visible(True)
        #
        # # As long as the indexation is being executed stay true, and then :
        # loading_box.set_visible(False)
        # query_box = builder.get_object("query_box")
        # query_box.set_visible(True)

        # When indexation is finished Change this to get vocabulary from inverted file
        # Eventualy manage exception if vocabular inexistent
        vocabulary = self.backend.inv_file.get_terms()

        liststore = Gtk.ListStore(str)
        for s in vocabulary:
            liststore.append([s])

        completion = Gtk.EntryCompletion()
        completion.set_model(liststore)
        completion.set_text_column(0)

        entry = builder.get_object("search_entry")
        entry.set_completion(completion)

        loading_box.set_visible(False)

        query_box.set_visible(True)

    def algo_combo_changed(self, combobox):
        print("Algo combo changed to " + combobox.get_active_text())
        self.query_parameters["algorithm"] = combobox.get_active_text()

    def results_number_changed(self, spinbutton):
        print("Results number changed to " + str(spinbutton.get_value_as_int()))
        self.query_parameters["results_number"] = spinbutton.get_value_as_int()

    def search_changed(self, searchentry):
        print("Search changed to " + searchentry.get_text())
        self.query_parameters["query"] = searchentry.get_text()

    def start_query(self, button):
        print("Start query")

        loading_box = builder.get_object("loading_box")
        loading_box.set_visible(True)

        results = self.backend.query(query=self.query_parameters["query"],
                           algorithm=self.query_parameters["algorithm"],
                           number_of_results=self.query_parameters["results_number"])

        stats = StatsControl.last_query()

        loading_box.set_visible(False)

        start_time_tofill = builder.get_object("start_time_tofill")
        start_time_tofill.set_text("{:%H:%M:%S.%f}".format(stats.start_time))

        end_time_tofill = builder.get_object("end_time_tofill")
        end_time_tofill.set_text("{:%H:%M:%S.%f}".format(stats.finish_time))

        end_time_tofill = builder.get_object("total_time_tofill")
        end_time_tofill.set_text("{}".format(stats.total_time))

        pl_accesses_tofill = builder.get_object("pl_accesses_tofill")
        pl_accesses_tofill.set_text(str(stats.pl_accesses))

        disk_accesses_tofill = builder.get_object("disk_accesses_tofill")
        disk_accesses_tofill.set_text(str(stats.memory_accesses))

        results_box = builder.get_object("results_box")
        results_box.set_visible(True)

        # DOCID [0]
        # Score [1]
        # Path [2]
        #documents = []
        #for result in results:
            #document

        # TODO Create query thread and call function within

builder = Gtk.Builder()
builder.add_from_file("../ui/main_ui.glade")
builder.connect_signals(Handler())

main_window = builder.get_object("main_window")
main_window.show()

Gtk.main()
