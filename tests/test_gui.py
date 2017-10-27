import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject
from os import walk
import threading
from executable import Executable
from stats import StatsControl

import xml.etree.cElementTree as et

class Handler:

    indexation_parameters = {
        "has_stemming": False,
        "has_stop_words_removal": False,
        "has_compression": False,
        "files_list": [],
        "ignore_case": False,
        "date_weight": 1,
        "title_weight": 1,
        "use_weights": False,
        "memory_limit": 50
    }

    query_parameters = {
        "algorithm": "NAIVE",
        "results_number": 5,
        "query": "",
        "similar_words_number": 5
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

    def toggle_stemming(self, button):
        print("Toggle stemming to " + str(button.get_active()))
        self.indexation_parameters["has_stemming"] = button.get_active()

    def toggle_stop_words_removal(self, button):
        print("Toggle stop words removal to " + str(button.get_active()))
        self.indexation_parameters["has_stop_words_removal"] = button.get_active()

    def toggle_ignore_case(self, button):
        print("Toggle ignore case to " + str(button.get_active()))
        self.indexation_parameters["ignore_case"] = button.get_active()

    def toggle_compression(self, button):
        print("Toggle compression to " + str(button.get_active()))
        self.indexation_parameters["has_compression"] = button.get_active()

    def memory_limit_changed(self, spinbutton):
        print("Memory Limit changed to " + str(spinbutton.get_value_as_int()))
        self.indexation_parameters["memory_limit"] = spinbutton.get_value_as_int()

    def toggle_weights_use(self, button):
        print("Toggle weights use to " + str(button.get_active()))
        self.indexation_parameters["use_weights"] = button.get_active()

        title_weight_grid = builder.get_object("title_weight_grid")
        title_weight_grid.set_visible(button.get_active())

        date_weight_grid = builder.get_object("date_weight_grid")
        date_weight_grid.set_visible(button.get_active())

    def title_weight_changed(self, spinbutton):
        print("Title weight changed to " + str(spinbutton.get_value_as_int()))
        self.indexation_parameters["title_weight"] = spinbutton.get_value_as_int()

    def date_weight_changed(self, spinbutton):
        print("Date weight changed to " + str(spinbutton.get_value_as_int()))
        self.indexation_parameters["date_weight"] = spinbutton.get_value_as_int()

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

    def call_backend_indexation(self):
        print("Indexation started !")
        self.backend.indexing(files=self.indexation_parameters["files_list"],
                              ignore_stop_words=self.indexation_parameters["has_stop_words_removal"],
                              stemming=self.indexation_parameters["has_stemming"],
                              use_vbytes=self.indexation_parameters["has_compression"],
                              ignore_case=self.indexation_parameters["ignore_case"],
                              date_weight=self.indexation_parameters["date_weight"],
                              title_weight=self.indexation_parameters["title_weight"],
                              use_weights=self.indexation_parameters["use_weights"],
                              memory_limit=self.indexation_parameters["memory_limit"]
                            )
        GLib.idle_add(self.on_indexation_complete)

    def start_indexation(self, button):
        print("Start indexation")

        if len(self.indexation_parameters["files_list"]) <= 0:
            print("No file has been specified !")
            return

        button.set_sensitive(False)

        loading_box = builder.get_object("loading_box")
        loading_box.set_visible(True)

        indexation_statistics_box = builder.get_object("indexation_statistics_box")
        query_box = builder.get_object("query_box")
        results_box = builder.get_object("results_box")
        similar_words_box = builder.get_object("similar_words_box")
        similar_words_box.set_visible(False)
        indexation_statistics_box.set_visible(False)
        query_box.set_visible(False)
        results_box.set_visible(False)

        thread = threading.Thread(target=self.call_backend_indexation)
        thread.daemon = True
        thread.start()


    def on_indexation_complete(self):
        print("Indexation complete !")

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

        loading_box = builder.get_object("loading_box")
        indexation_statistics_box = builder.get_object("indexation_statistics_box")
        query_box = builder.get_object("query_box")
        start_indexation_button = builder.get_object("start_indexation_button")

        loading_box.set_visible(False)

        indexation_stats = StatsControl.last_indexing()

        indexation_start_time_tofill = builder.get_object("indexation_start_time_tofill")
        indexation_start_time_tofill.set_text("{:%H:%M:%S.%f}".format(indexation_stats.start_time))

        indexation_end_time_tofill = builder.get_object("indexation_end_time_tofill")
        indexation_end_time_tofill.set_text("{:%H:%M:%S.%f}".format(indexation_stats.finish_time))

        indexation_total_time_tofill = builder.get_object("indexation_total_time_tofill")
        indexation_total_time_tofill.set_text("{}".format(indexation_stats.total_time))

        indexation_file_size_tofill = builder.get_object("indexation_file_size_tofill")
        indexation_file_size_tofill.set_text(str(indexation_stats.file_size))

        indexation_statistics_box.set_visible(True)

        query_box.set_visible(True)

        start_indexation_button.set_sensitive(True)

    def algo_combo_changed(self, combobox):
        print("Algo combo changed to " + combobox.get_active_text())
        self.query_parameters["algorithm"] = combobox.get_active_text()

    def results_number_changed(self, spinbutton):
        print("Results number changed to " + str(spinbutton.get_value_as_int()))
        self.query_parameters["results_number"] = spinbutton.get_value_as_int()

    def similar_words_number_changed(self, spinbutton):
        print("Similar words number changed to " + str(spinbutton.get_value_as_int()))
        self.query_parameters["similar_words_number"] = spinbutton.get_value_as_int()

    def search_changed(self, searchentry):
        query = searchentry.get_text()
        print("Search changed to " + query)
        self.query_parameters["query"] = query

        start_query_button = builder.get_object("start_query_button")
        display_similar_words_button = builder.get_object("display_similar_words_button")

        if query == "":
            start_query_button.set_sensitive(False)
            display_similar_words_button.set_sensitive(False)
        elif len(query.split()) == 1:
            start_query_button.set_sensitive(True)
            display_similar_words_button.set_sensitive(True)
        else:
            start_query_button.set_sensitive(True)
            display_similar_words_button.set_sensitive(False)



    def call_backend_query(self):
        print("Query started !")

        results = self.backend.query(query=self.query_parameters["query"],
                                     algorithm=self.query_parameters["algorithm"],
                                     number_of_results=self.query_parameters["results_number"])
        GLib.idle_add(self.on_query_complete, results)

    def start_query(self, button):
        print("Start query")

        if self.query_parameters["query"] == "":
            print("No query has been specified !")
            return

        button.set_sensitive(False)

        loading_box = builder.get_object("loading_box")
        loading_box.set_visible(True)

        print("Dict : {}".format(self.query_parameters))

        thread = threading.Thread(target=self.call_backend_query)
        thread.daemon = True
        thread.start()

    def on_query_complete(self, results):
        print("Query complete !")

        query_stats = StatsControl.last_query()

        loading_box = builder.get_object("loading_box")
        loading_box.set_visible(False)

        start_time_tofill = builder.get_object("start_time_tofill")
        start_time_tofill.set_text("{:%H:%M:%S.%f}".format(query_stats.start_time))

        end_time_tofill = builder.get_object("end_time_tofill")
        end_time_tofill.set_text("{:%H:%M:%S.%f}".format(query_stats.finish_time))

        total_time_tofill = builder.get_object("total_time_tofill")
        total_time_tofill.set_text("{}".format(query_stats.total_time))

        pl_accesses_tofill = builder.get_object("pl_accesses_tofill")
        pl_accesses_tofill.set_text(str(query_stats.pl_accesses))

        disk_accesses_tofill = builder.get_object("disk_accesses_tofill")
        disk_accesses_tofill.set_text(str(query_stats.memory_accesses))

        results_text = "\t Score     |\tDOCID   |\t   File path \n"
        for result in results:
            results_text += ("\t{:8.5f} |\t{:8} |\t{}".format(result[1], result[0], result[2])) + "\n"

        print("results" + results_text)

        results_textview = builder.get_object("results_textview")
        results_textview_buffer = results_textview.get_buffer()
        results_textview_buffer.set_text(results_text)

        results_box = builder.get_object("results_box")
        results_box.set_visible(True)

        start_query_button = builder.get_object("start_query_button")
        start_query_button.set_sensitive(True)

    def call_backend_similar_search(self):
        print("Similar search started !")

        results = self.backend.random_indexing(choice_key=self.query_parameters["query"],
                                               top_results=self.query_parameters["similar_words_number"])
        GLib.idle_add(self.on_similar_search_complete, results)

    def start_similar_search(self, button):
        print("Start query")

        query = self.query_parameters["query"]

        # Just in case, check if the query is only a single word, otherwise random indexing querying doesn't work
        if len(query.split()) > 1 or query == "":
            print("Can only find similar words to a single word !")
            return

        button.set_sensitive(False)

        similar_words_box = builder.get_object("similar_words_box")
        similar_words_box.set_visible(False)

        thread = threading.Thread(target=self.call_backend_similar_search)
        thread.daemon = True
        thread.start()

    def on_similar_search_complete(self, results):
        print("Query complete !")

        display_similar_words_button = builder.get_object("display_similar_words_button")
        display_similar_words_button.set_sensitive(True)

        results_text = str(results)

        similar_words_textview = builder.get_object("similar_words_textview")
        similar_words_textview_buffer = similar_words_textview.get_buffer()
        similar_words_textview_buffer.set_text(results_text)

        similar_words_box = builder.get_object("similar_words_box")
        similar_words_box.set_visible(True)


builder = Gtk.Builder()
builder.add_from_file("../ui/main_ui.glade")
builder.connect_signals(Handler())

main_window = builder.get_object("main_window")
main_window.show()
main_window.connect("delete-event", Gtk.main_quit)
Gtk.main()
