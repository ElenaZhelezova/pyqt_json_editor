import sys
import json
import PyQt5.QtWidgets as pt


CONST_DATA = {
            'version': 1,
            'places': [{'template': 'mas_ops', 'id': '',
                        'setup': {'filial': '', 'reg': '', 'system_host': '',
                                  'mas': {'db': {'host': '', 'password': '', 'service_pass': ''}},
                                  'easops': {'db': {'host': '', 'password': '', 'service_pass': ''}}
                                  },
                        'win': []        # {'id': 0, 'template': 'mas_chief'}, {'id': 1, 'template': 'mas_operational'}
                        }]
        }


class JSONEditor(pt.QWidget):
    def __init__(self, data=CONST_DATA):
        super().__init__()
        self.data = data
        self.initUI(self.data)

    def initUI(self, data):
        grid = pt.QGridLayout()
        grid.setSpacing(5)

        save_file_btn = pt.QPushButton('Save')
        save_file_btn.clicked.connect(self.save_values_to_file)

        hbox = pt.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(save_file_btn)

        titles = ['id', 'filial', 'region', 'system host', 'mas db host', 'mas db password', 'mas db service password',
                  'easop db host', 'easop db password', 'easop db service password', 'win']

        for i in range(len(titles)):
            grid.addWidget(pt.QLabel(titles[i]), i, 0)

        self.id_edit = pt.QLineEdit(str(data['places'][0]['id']))
        grid.addWidget(self.id_edit, 0, 1)
        self.filial_edit = pt.QLineEdit(str(data['places'][0]['setup']['filial']))
        grid.addWidget(self.filial_edit, 1, 1)
        self.region_edit = pt.QLineEdit(str(data['places'][0]['setup']['reg']))
        grid.addWidget(self.region_edit, 2, 1)
        self.sys_host_edit = pt.QLineEdit(data['places'][0]['setup']['system_host'])
        grid.addWidget(self.sys_host_edit, 3, 1)
        self.mas_db_host_edit = pt.QLineEdit(data['places'][0]['setup']['mas']['db']['host'])
        grid.addWidget(self.mas_db_host_edit, 4, 1)
        self.mas_db_pass_edit = pt.QLineEdit(data['places'][0]['setup']['mas']['db']['password'])
        grid.addWidget(self.mas_db_pass_edit, 5, 1)
        self.mas_db_service_pass_edit = pt.QLineEdit(data['places'][0]['setup']['mas']['db']['service_pass'])
        grid.addWidget(self.mas_db_service_pass_edit, 6, 1)
        self.easop_db_host_edit = pt.QLineEdit(data['places'][0]['setup']['easops']['db']['host'])
        grid.addWidget(self.easop_db_host_edit, 7, 1)
        self.easop_db_pass_edit = pt.QLineEdit(data['places'][0]['setup']['easops']['db']['password'])
        grid.addWidget(self.easop_db_pass_edit, 8, 1)
        self.easop_db_service_pass_edit = pt.QLineEdit(data['places'][0]['setup']['easops']['db']['service_pass'])
        grid.addWidget(self.easop_db_service_pass_edit, 9, 1)
        self.win_edit = pt.QLineEdit(str(len(data['places'][0]['win'])))
        grid.addWidget(self.win_edit, 10, 1)
        grid.addLayout(hbox, 11, 1)

        self.setLayout(grid)

    def error_message(self, msg_txt):
        msg = pt.QMessageBox()
        msg.setIcon(pt.QMessageBox.Critical)
        msg.setText("Value Error")
        msg.setInformativeText(msg_txt)
        msg.setWindowTitle("Error")
        msg.exec_()

    def save_values_to_file(self):
        file_name = pt.QFileDialog.getSaveFileName(self, 'Save file', './')[0] + '.json'

        data_to_save = CONST_DATA

        try:
            data_to_save['places'][0]['id'] = int(self.id_edit.text())
        except ValueError:
            return self.error_message('Expected integer in "id" field')

        try:
            data_to_save['places'][0]['setup']['filial'] = int(self.filial_edit.text())
        except ValueError:
            return self.error_message('Expected integer in "filial" field')

        try:
            data_to_save['places'][0]['setup']['reg'] = int(self.region_edit.text())
        except ValueError:
            return self.error_message('Expected integer in "region" field')

        data_to_save['places'][0]['setup']['system_host'] = self.sys_host_edit.text()
        data_to_save['places'][0]['setup']['mas']['db']['host'] = self.mas_db_host_edit.text()
        data_to_save['places'][0]['setup']['mas']['db']['password'] = self.mas_db_pass_edit.text()
        data_to_save['places'][0]['setup']['mas']['db']['service_pass'] = self.mas_db_service_pass_edit.text()
        data_to_save['places'][0]['setup']['easops']['db']['host'] = self.easop_db_host_edit.text()
        data_to_save['places'][0]['setup']['easops']['db']['password'] = self.easop_db_pass_edit.text()
        data_to_save['places'][0]['setup']['easops']['db']['service_pass'] = self.easop_db_service_pass_edit.text()

        if int(self.win_edit.text()) > 0:
            data_to_save['places'][0]['win'].append({'id': 0, 'template': 'mas_chief'})
            if int(self.win_edit.text()) > 1:
                for i in range (1, int(self.win_edit.text())):
                    data_to_save['places'][0]['win'].append({'id': 1, 'template': 'mas_operational'})

        with open(file_name, 'w') as f:
            json.dump(data_to_save, f)


class MainWin(pt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('Editing file')

        self.text_edit = JSONEditor()
        self.setCentralWidget(self.text_edit)

        opn_file = pt.QAction('Open..', self)
        opn_file.setShortcut('Ctrl+O')
        opn_file.triggered.connect(self.show_open_dialog)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(opn_file)

    def show_open_dialog(self):
        f_name = pt.QFileDialog.getOpenFileName(self, 'Open file', './')[0]
        with open(f_name) as f:
            jsn_data = json.load(f)
            self.text_edit = JSONEditor(jsn_data)
            self.setCentralWidget(self.text_edit)

    def closeEvent(self, event):
        reply = pt.QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     pt.QMessageBox.Yes | pt.QMessageBox.No, pt.QMessageBox.No)
        if reply == pt.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = pt.QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())