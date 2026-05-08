import os
import winreg
import ctypes
import wx

class AdvancedPathManager(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Windows Path Editor - Advanced', size=(700, 600))
        self.panel = wx.Panel(self)
        self.reg_path = "Environment"
        
        self.init_ui()
        self.setup_shortcuts()
        self.load_current_paths()
        self.Centre()

    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # --- 1. Top Section: Path List (Priority) ---
        list_label = wx.StaticText(self.panel, label="Current Environment Paths (Priority: Top to Bottom):")
        list_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        list_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.path_list = wx.ListBox(self.panel, style=wx.LB_SINGLE)
        
        # Control Buttons with Shortcut Hints
        ctrl_btn_sizer = wx.BoxSizer(wx.VERTICAL)
        self.btn_up = wx.Button(self.panel, label="Move Up [Alt+Up]")
        self.btn_down = wx.Button(self.panel, label="Move Down [Alt+Down]")
        self.btn_delete = wx.Button(self.panel, label="Delete [Del]")
        
        self.btn_up.Bind(wx.EVT_BUTTON, self.on_move_up)
        self.btn_down.Bind(wx.EVT_BUTTON, self.on_move_down)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        self.btn_delete.SetForegroundColour(wx.RED)

        ctrl_btn_sizer.Add(self.btn_up, 0, wx.EXPAND|wx.BOTTOM, 5)
        ctrl_btn_sizer.Add(self.btn_down, 0, wx.EXPAND|wx.BOTTOM, 5)
        ctrl_btn_sizer.Add(self.btn_delete, 0, wx.EXPAND|wx.BOTTOM, 5)

        list_sizer.Add(self.path_list, 1, wx.EXPAND|wx.RIGHT, 10)
        list_sizer.Add(ctrl_btn_sizer, 0, wx.EXPAND)

        # --- 2. Middle Section: Add New Path ---
        add_box = wx.StaticBox(self.panel, label="Add New Path")
        add_sizer = wx.StaticBoxSizer(add_box, wx.HORIZONTAL)
        self.path_input = wx.TextCtrl(self.panel)
        browse_btn = wx.Button(self.panel, label="Browse...")
        add_btn = wx.Button(self.panel, label="Add to List")
        
        browse_btn.Bind(wx.EVT_BUTTON, self.on_browse)
        add_btn.Bind(wx.EVT_BUTTON, self.on_add)

        add_sizer.Add(self.path_input, 1, wx.ALL|wx.EXPAND, 5)
        add_sizer.Add(browse_btn, 0, wx.ALL, 5)
        add_sizer.Add(add_btn, 0, wx.ALL, 5)

        # --- 3. Bottom Section: Save ---
        self.btn_save = wx.Button(self.panel, label="SAVE ALL CHANGES TO WINDOWS", size=(-1, 60))
        self.btn_save.SetBackgroundColour(wx.Colour(0, 100, 0))
        self.btn_save.SetForegroundColour(wx.WHITE)
        self.btn_save.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save_registry)

        # Final Layout
        main_sizer.Add(list_label, 0, wx.LEFT|wx.TOP, 15)
        main_sizer.Add(list_sizer, 1, wx.EXPAND|wx.ALL, 15)
        main_sizer.Add(add_sizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 15)
        main_sizer.Add(self.btn_save, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        self.status_bar = self.CreateStatusBar()
        self.panel.SetSizer(main_sizer)

    def setup_shortcuts(self):
        """ Register Global Hotkeys """
        ID_UP = wx.NewIdRef()
        ID_DOWN = wx.NewIdRef()
        ID_DEL = wx.NewIdRef()

        entries = [
            wx.AcceleratorEntry(wx.ACCEL_ALT, wx.WXK_UP, ID_UP),
            wx.AcceleratorEntry(wx.ACCEL_ALT, wx.WXK_DOWN, ID_DOWN),
            wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_DELETE, ID_DEL)
        ]
        
        self.SetAcceleratorTable(wx.AcceleratorTable(entries))

        self.Bind(wx.EVT_MENU, self.on_move_up, id=ID_UP)
        self.Bind(wx.EVT_MENU, self.on_move_down, id=ID_DOWN)
        self.Bind(wx.EVT_MENU, self.on_delete, id=ID_DEL)

    def load_current_paths(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.reg_path, 0, winreg.KEY_READ)
            path_string, _ = winreg.QueryValueEx(key, "Path")
            winreg.CloseKey(key)
            paths = [p.strip() for p in path_string.split(';') if p.strip()]
            self.path_list.Set(paths)
            self.status_bar.SetStatusText(f"Loaded {len(paths)} paths. Use Alt+Up/Down to reorder.")
        except Exception as e:
            wx.MessageBox(f"Error loading Registry: {e}", "Error", wx.ICON_ERROR)

    def on_browse(self, event):
        with wx.DirDialog(self, "Select Folder") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.path_input.SetValue(dlg.GetPath())

    def on_add(self, event):
        new_path = self.path_input.GetValue().strip()
        if new_path and os.path.exists(new_path):
            if new_path not in self.path_list.GetStrings():
                self.path_list.Append(new_path)
                self.path_input.Clear()
                self.path_list.SetSelection(self.path_list.GetCount() - 1)
            else:
                wx.MessageBox("This path is already in the list.", "Duplicate", wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Invalid directory path.", "Error", wx.ICON_WARNING)

    def on_delete(self, event):
        sel = self.path_list.GetSelection()
        if sel != wx.NOT_FOUND:
            self.path_list.Delete(sel)
            if sel < self.path_list.GetCount():
                self.path_list.SetSelection(sel)
            elif self.path_list.GetCount() > 0:
                self.path_list.SetSelection(sel - 1)

    def on_move_up(self, event):
        sel = self.path_list.GetSelection()
        if sel > 0:
            text = self.path_list.GetString(sel)
            self.path_list.Delete(sel)
            self.path_list.Insert(text, sel - 1)
            self.path_list.SetSelection(sel - 1)

    def on_move_down(self, event):
        sel = self.path_list.GetSelection()
        if sel < self.path_list.GetCount() - 1 and sel != wx.NOT_FOUND:
            text = self.path_list.GetString(sel)
            self.path_list.Delete(sel)
            self.path_list.Insert(text, sel + 1)
            self.path_list.SetSelection(sel + 1)

    def on_save_registry(self, event):
        all_paths = self.path_list.GetStrings()
        final_string = ";".join(all_paths)
        
        confirm = wx.MessageBox(
            "Are you sure you want to write these changes to the Windows Registry?", 
            "Confirm Save", 
            wx.YES_NO | wx.ICON_QUESTION
        )
        
        if confirm == wx.YES:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.reg_path, 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, final_string)
                winreg.CloseKey(key)
                
                # Broadcast environment change
                ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 0x02, 1000, ctypes.byref(ctypes.c_long()))
                wx.MessageBox("System Path updated successfully!", "Success", wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Failed to save changes: {e}", "Registry Error", wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    AdvancedPathManager().Show()
    app.MainLoop()