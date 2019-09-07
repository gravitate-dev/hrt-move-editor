import os
import json

from data.MoveListData import MoveListData


class ModController:

    def __init__(self):
        self._mod_lists = []

    def load(self, mod_base_path):
        self._mod_lists = []
        mod_folders = [f.path for f in os.scandir(mod_base_path) if
                       f.is_dir() and not f.path.split(os.sep)[-1].startswith("_")]

        for mf in mod_folders:
            self._extract_mod_list_from_folder(mf)

    def _extract_mod_list_from_folder(self, mod_folder_path):
        file_load_path = mod_folder_path + os.sep + "_FilesToLoad.json";
        if not os.path.exists(file_load_path):
            return None
        with open(file_load_path) as f:
            content = json.load(f);
            if "moveFiles" not in content:
                return None
            move_files = content["moveFiles"]
            for mf in move_files:
                move_file_full_path = mod_folder_path + os.sep + mf
                if not os.path.exists(move_file_full_path):
                    continue
                move_data = MoveListData(move_file_full_path)
                move_data.checkAndMakeBackup()
                self._mod_lists.append(move_data)

    def remove_move(self, mod_filename, mod_move):
        chosen_mod = self._get_mod_by_name(mod_filename)
        if chosen_mod == None:
            return
        return chosen_mod.remove_move_from_player(mod_move)

    def add_move(self, mod_filename, mod_move):
        chosen_mod = self._get_mod_by_name(mod_filename)
        if chosen_mod == None:
            return
        chosen_mod.add_move_to_player(mod_move)

    def restore_all_moves(self, mod_filename):
        chosen_mod = self._get_mod_by_name(mod_filename)
        if chosen_mod == None:
            return
        chosen_mod.restore_all_moves()

    def restore_everything(self):
        for mod in self._mod_lists:
            mod.restore_all_moves()

    def _get_mod_by_name(self, mod_filename):
        for mod in self._mod_lists:
            if mod.mod_filename == mod_filename:
                return mod
        return None

    def save(self):
        for mod_list in self._mod_lists:
            mod_list.save()

    def get_mod_lists(self):
        return self._mod_lists;
