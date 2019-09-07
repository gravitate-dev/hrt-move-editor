import os
import json


class MoveListData:
    def __init__(self, mod_path):
        self.full_mod_path = mod_path;
        self.mod_filename = mod_path.split(os.sep)[-2]+os.sep+mod_path.split(os.sep)[-1]
        print(self.mod_filename)
        self.full_mod_backup_path = self.full_mod_path.replace(".json", ".backup.json")

        with open(self.full_mod_path) as f:
            self.player_moves_content = json.load(f);

        # makes a backup file of the movelistdata
        if not os.path.exists(self.full_mod_backup_path):
            with open(self.full_mod_backup_path, "w") as f:
                json.dump(self.player_moves_content, f, indent=4)

        with open(self.full_mod_path) as f:
            self.all_moves_content = json.load(f);

    def get_player_moves(self):
        return self.player_moves_content

    def get_all_moves(self):
        return self.all_moves_content

    def get_move_delta(self):
        player = list(self.player_moves_content.keys())
        backup = list(self.all_moves_content.keys())
        boolean_map = {}
        for move in backup:
            boolean_map[move] = False
        for move in player:
            if move in boolean_map:
                boolean_map[move] = True

        return boolean_map

    def restore_all_moves(self):
        self.player_moves_content = self.all_moves_content

    def save(self):
        with open(self.full_mod_path, "w") as f:
            json.dump(self.player_moves_content, f, indent=4)

    def add_move_to_player(self, move_name):
        if move_name in self.all_moves_content:
            self.player_moves_content[move_name] = self.all_moves_content[move_name]

    def remove_move_from_player(self, move_name):
        if move_name in self.player_moves_content:
            del self.player_moves_content[move_name]

    def checkAndMakeBackup(self):
        if os.path.exists(self.full_mod_backup_path):
            return
        with open(self.full_mod_backup_path, "w") as f:
            json.dump(self.content, f, indent=4)
