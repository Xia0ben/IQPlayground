import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject
from os import walk
import threading
import time

class Handler:

    indexation_parameters = {
        "has_stemming": False,
        "has_stop_words_removal": False,
        "has_compression": False,
        "files_list": []
    }

    query_parameters = {
        "algorithm": "Naive",
        "results_number": 5,
        "query": ""
    }

    state = {
        "indexation_done": False,
        "query_complete": False
    }

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
        vocabulary = ["washington", "monaco", "washing"]

        liststore = Gtk.ListStore(str)
        for s in vocabulary:
            liststore.append([s])

        completion = Gtk.EntryCompletion()
        completion.set_model(liststore)
        completion.set_text_column(0)

        entry = builder.get_object("search_entry")
        entry.set_completion(completion)

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

        # Create query thread and call function within

builder = Gtk.Builder()
builder.add_from_file("../ui/main_ui.glade")
builder.connect_signals(Handler())

main_window = builder.get_object("main_window")
main_window.show()

Gtk.main()

