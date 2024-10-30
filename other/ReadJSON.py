import json

from body_parts.Framework import Framework
from body_parts.UpperPanel import UpperPanel
from body_parts.MiddlePanel import MiddlePanel
from body_parts.LowerPanel import LowerPanel
from body_parts.Armrest import Armrest
from body_parts.CupHolder import CupHolder
from Body import Body

from qt_classes.CarBodyGroupBox import CarBodyGroupBox

class ReadJSON():

    def __init__(self, file_name: list):

        self.file_name = file_name

    def parse_json(self, gui):

        if self.file_name[0] != "" and self.file_name[0].endswith(".json"):
            with open(self.file_name[0], "r", encoding="UTF-8") as file:
                body_configs = json.load(file)

            if gui.body_counter == 0:
                gui.outer_layout.removeWidget(gui.starting_label)
                gui.starting_label.deleteLater()

            for index, body_config in enumerate(body_configs):

                body_tmp = Body(gui.body_counter, upper_panel=UpperPanel("", ""), 
                    middle_panel=MiddlePanel(""), 
                    lower_panel=LowerPanel("", "", ""),
                    armrest=Armrest("", "", ""),
                    cup_holder=CupHolder("", ""),
                    framework=Framework("", "")
                    )
                
                body_tmp = self.assign_body_parts(body_tmp, body_config)
                gui.list_of_bodys.append(body_tmp)
                gui.mpl_widget.update_plot(gui.list_of_bodys[gui.body_counter])

                self.add_new_cb_group_box(gui, body_tmp)

                gui.body_counter += 1

    def assign_body_parts(self, body_tmp: Body, body_config):

        body_tmp.framework.material = body_config['body']['framework']['material']
        body_tmp.framework.color = body_config['body']['framework']['color']

        body_tmp.upper_panel.is_controlable = body_config['body']['upper_panel']['is_controllable']
        body_tmp.upper_panel.ac_type = body_config['body']['upper_panel']['type']

        body_tmp.middle_panel.functionality = body_config['body']['middle_panel']['functionality']

        body_tmp.lower_panel.functionality = body_config['body']['lower_panel']['functionality']
        body_tmp.lower_panel.is_cup = body_config['body']['lower_panel']['is_cup']
        body_tmp.lower_panel.color = body_config['body']['lower_panel']['color']

        body_tmp.armrest.heating = body_config['body']['armrest']['heating']
        body_tmp.armrest.material = body_config['body']['armrest']['material']
        body_tmp.armrest.color = body_config['body']['armrest']['color']

        body_tmp.cup_holder.usb_socket = body_config['body']['cup_holder']['usb_socket']
        body_tmp.cup_holder.color = body_config['body']['cup_holder']['color']

        return body_tmp
    
    def add_new_cb_group_box(self, gui, body_tmp):
        gui.list_of_car_body_group_box.append(CarBodyGroupBox(body_tmp))

        gui.list_of_car_body_group_box[gui.body_counter].button_plan.clicked.connect(
            lambda _, x=gui.list_of_car_body_group_box[gui.body_counter].body.body_id: gui.pb_plan_clicked(x))
        gui.list_of_car_body_group_box[gui.body_counter].button_schedule.clicked.connect(
            lambda _, x=gui.list_of_car_body_group_box[gui.body_counter].body.body_id: gui.pb_schedule_clicked(x))
        gui.list_of_car_body_group_box[gui.body_counter].button_ready.clicked.connect(
            lambda _, x=gui.list_of_car_body_group_box[gui.body_counter].body.body_id: gui.pb_ready_clicked(x))
        gui.list_of_car_body_group_box[gui.body_counter].button_remove.clicked.connect(
            lambda _, x=gui.list_of_car_body_group_box[gui.body_counter].body.body_id: gui.pb_delete_clicked(x))
        
        gui.outer_layout.addWidget(gui.list_of_car_body_group_box[gui.body_counter].group_box)

