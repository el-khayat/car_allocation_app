import wx
import sqlite3

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)

        self.panel = wx.Panel(self)

        # Créez des champs de texte pour saisir les données du client
        self.full_name_label = wx.StaticText(self.panel, label="Full Name:")
        self.full_name_text = wx.TextCtrl(self.panel)

        self.address_label = wx.StaticText(self.panel, label="Address:")
        self.address_text = wx.TextCtrl(self.panel)

        self.phone_label = wx.StaticText(self.panel, label="Phone:")
        self.phone_text = wx.TextCtrl(self.panel)

        self.email_label = wx.StaticText(self.panel, label="Email:")
        self.email_text = wx.TextCtrl(self.panel)

        self.cin_label = wx.StaticText(self.panel, label="CIN:")
        self.cin_text = wx.TextCtrl(self.panel)

        # Bouton pour enregistrer le client
        self.save_button = wx.Button(self.panel, label="Enregistrer le Client")
        self.Bind(wx.EVT_BUTTON, self.save_client, self.save_button)

        # Bouton pour rafraîchir la liste des clients
        self.refresh_button = wx.Button(self.panel, label="Rafraîchir la liste")
        self.Bind(wx.EVT_BUTTON, self.refresh_clients, self.refresh_button)

        # Bouton pour supprimer le client
        self.delete_button = wx.Button(self.panel, label="Supprimer le Client")
        self.Bind(wx.EVT_BUTTON, self.delete_client, self.delete_button)

        # Bouton pour mettre à jour le client
        self.update_button = wx.Button(self.panel, label="Mettre à jour le Client")
        self.Bind(wx.EVT_BUTTON, self.update_client, self.update_button)

        # Créez une liste pour afficher les clients
        self.client_list = wx.ListCtrl(self.panel, style=wx.LC_REPORT)
        self.client_list.InsertColumn(0, "ID")
        self.client_list.InsertColumn(1, "Full Name")
        self.client_list.InsertColumn(2, "Address")
        self.client_list.InsertColumn(3, "Phone")
        self.client_list.InsertColumn(4, "Email")
        self.client_list.InsertColumn(5, "CIN")

        # Ajoutez les contrôles au sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.full_name_label, 0, wx.ALL, 5)
        self.sizer.Add(self.full_name_text, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.address_label, 0, wx.ALL, 5)
        self.sizer.Add(self.address_text, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.phone_label, 0, wx.ALL, 5)
        self.sizer.Add(self.phone_text, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.email_label, 0, wx.ALL, 5)
        self.sizer.Add(self.email_text, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.cin_label, 0, wx.ALL, 5)
        self.sizer.Add(self.cin_text, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.save_button, 0, wx.ALL, 5)
        self.sizer.Add(self.refresh_button, 0, wx.ALL, 5)
        self.sizer.Add(self.delete_button, 0, wx.ALL, 5)
        self.sizer.Add(self.update_button, 0, wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self.panel, -1), 0, wx.EXPAND|wx.ALL, 5)  # Ligne de séparation
        self.sizer.Add(self.client_list, 1, wx.EXPAND|wx.ALL, 5)

        # Définir le sizer pour le panneau
        self.panel.SetSizer(self.sizer)

        # Initialiser la connexion à la base de données
        self.conn = sqlite3.connect("car_allocation.db")
        self.cursor = self.conn.cursor()

        # Rafraîchir la liste des clients au démarrage
        self.refresh_clients(None)

        # Variable pour stocker l'ID du client sélectionné
        self.selected_client_id = None

        # Liens d'événements pour la liste
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_client, self.client_list)

    def on_select_client(self, event):
        # Récupérer l'ID du client sélectionné dans la liste
        selected_item = event.GetIndex()
        self.selected_client_id = int(self.client_list.GetItemText(selected_item, 0))

        # Récupérer les données du client sélectionné
        self.full_name_text.SetValue(self.client_list.GetItemText(selected_item, 1))
        self.address_text.SetValue(self.client_list.GetItemText(selected_item, 2))
        self.phone_text.SetValue(self.client_list.GetItemText(selected_item, 3))
        self.email_text.SetValue(self.client_list.GetItemText(selected_item, 4))
        self.cin_text.SetValue(self.client_list.GetItemText(selected_item, 5))

    def refresh_clients(self, event):
        # Effacer les anciennes entrées de la liste
        self.client_list.DeleteAllItems()

        # Récupérer tous les clients de la base de données
        self.cursor.execute("SELECT * FROM clients")
        clients = self.cursor.fetchall()

        # Ajouter chaque client à la liste
        for row_id, client in enumerate(clients):
            self.client_list.InsertItem(row_id, str(client[0]))
            for col_id, value in enumerate(client[1:]):
                self.client_list.SetItem(row_id, col_id + 1, str(value))

    def save_client(self, event):
        # Récupérer les données des champs de texte
        full_name = self.full_name_text.GetValue()
        address = self.address_text.GetValue()
        phone = self.phone_text.GetValue()
        email = self.email_text.GetValue()
        cin = self.cin_text.GetValue()

        # Insérer les données dans la base de données
        self.cursor.execute(
            "INSERT INTO clients (full_name, address, phone, email, cin) VALUES (?, ?, ?, ?, ?)",
            (full_name, address, phone, email, cin),
        )

        # Commit des changements et fermeture de la connexion
        self.conn.commit()

        # Effacer les champs de texte après l'enregistrement
        self.full_name_text.SetValue("")
        self.address_text.SetValue("")
        self.phone_text.SetValue("")
        self.email_text.SetValue("")
        self.cin_text.SetValue("")

        # Rafraîchir la liste après l'ajout
        self.refresh_clients(None)

    def delete_client(self, event):
        # Vérifier si un client est sélectionné
        if self.selected_client_id is not None:
            # Supprimer le client de la base de données
            self.cursor.execute("DELETE FROM clients WHERE id=?", (self.selected_client_id,))

            # Commit des changements et fermeture de la connexion
            self.conn.commit()

            # Effacer les champs de texte après la suppression
            self.full_name_text.SetValue("")
            self.address_text.SetValue("")
            self.phone_text.SetValue("")
            self.email_text.SetValue("")
            self.cin_text.SetValue("")

            # Rafraîchir la liste après la suppression
            self.refresh_clients(None)

            # Réinitialiser l'ID du client sélectionné
            self.selected_client_id = None
        else:
            wx.MessageBox("Veuillez sélectionner un client à supprimer.", "Avertissement", wx.OK | wx.ICON_WARNING)

    def update_client(self, event):
        # Vérifier si un client est sélectionné
        if self.selected_client_id is not None:
            # Récupérer les données des champs de texte
            full_name = self.full_name_text.GetValue()
            address = self.address_text.GetValue()
            phone = self.phone_text.GetValue()
            email = self.email_text.GetValue()
            cin = self.cin_text.GetValue()

            # Mettre à jour le client dans la base de données
            self.cursor.execute(
                "UPDATE clients SET full_name=?, address=?, phone=?, email=?, cin=? WHERE id=?",
                (full_name, address, phone, email, cin, self.selected_client_id),
            )

            # Commit des changements et fermeture de la connexion
            self.conn.commit()

            # Effacer les champs de texte après la mise à jour
            self.full_name_text.SetValue("")
            self.address_text.SetValue("")
            self.phone_text.SetValue("")
            self.email_text.SetValue("")
            self.cin_text.SetValue("")

            # Rafraîchir la liste après la mise à jour
            self.refresh_clients(None)

            # Réinitialiser l'ID du client sélectionné
            self.selected_client_id = None
        else:
            wx.MessageBox("Veuillez sélectionner un client à mettre à jour.", "Avertissement", wx.OK | wx.ICON_WARNING)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, wx.ID_ANY, "Liste et Enregistrement des Clients")
    frame.Show()
    app.MainLoop()
