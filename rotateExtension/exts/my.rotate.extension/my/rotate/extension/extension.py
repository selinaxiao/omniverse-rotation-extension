
import omni.ext
import omni.ui as ui
import omni.kit.commands
import omni.kit.app.impl
from pxr import Sdf, Gf

import carb.events
import omni.appwindow

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.

# This extension can only be used on Prim objects, it will do nothing if run on other objects like materials 
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    state = 0

    def on_startup(self, ext_id):
        print("[my.rotate.extension] MyExtension startup")

        self.h_option = 1
        self.v_option = 1 
        self._app = omni.kit.app.get_app()

        if omni.appwindow.get_default_app_window().get_window() is not None:
            self._update_sub = self._app.get_update_event_stream().create_subscription_to_pop(
                self._on_update, name="cursor"
            )

        self._window = ui.Window("rotation display", width=500, height=300)
        with self._window.frame:
            with ui.VStack():       
                with ui.HStack():
                    ui.Label("Horizontal Rotation Speed", alignment=ui.Alignment.H_CENTER)
                    self.combobox1 = ui.ComboBox(1, "slow", "medium", "fast", alignment=ui.Alignment.H_CENTER)
               
                with ui.HStack():
                    ui.Label("Vertical Rotation Speed", alignment=ui.Alignment.H_CENTER)
                    self.combobox2 = ui.ComboBox(1, "slow", "medium", "fast", alignment=ui.Alignment.H_CENTER)

                ui.Button("Start", clicked_fn=self.on_click1)
                ui.Button("Stop", clicked_fn=self.on_click2)

    def udpate_movement(self):
        context = omni.usd.get_context()
        stage = context.get_stage()
        # print(context.get_selection().get_selected_prim_paths())
        prims = [stage.GetPrimAtPath(m) for m in context.get_selection().get_selected_prim_paths()]

        if prims == []:
            pass

        if self.state == 1:
            for i in range(len(prims)):
             
                current_prim = prims[i].GetAttribute('xformOp:rotateXYZ').Get()
              
                print(prims[i].GetAttribute('xformOp:rotateXYZ'))

                scale = 2
                omni.kit.commands.execute(
                    'ChangeProperty',
                    prop_path=Sdf.Path(str(prims[i].GetPrimPath())+'.xformOp:rotateXYZ'),
                    value=Gf.Vec3d((current_prim[0]+scale*(self.h_option+1)) % 360, current_prim[1], 
                (current_prim[2]+scale*(self.v_option+1)) % 360),
                    prev=current_prim 
                    )
        else:
            pass

    def on_click1(self):
        self.h_option = self.combobox1.model.get_item_value_model().get_value_as_int()
        self.v_option = self.combobox2.model.get_item_value_model().get_value_as_int()
        
        print(self.h_option, self.v_option)

        self.state = 1
        self.udpate_movement()

        # context = omni.usd.get_context()
        # stage = context.get_stage()
        # prims = [stage.GetPrimAtPath(m) for m in context.get_selection().get_selected_prim_paths()]
        # for i in range(len(prims)):
        #     current_prim = prims[i].GetAttributes()[8].Get()
        #     scale = 1
        #     omni.kit.commands.execute(
        #         'ChangeProperty',
        #         prop_path=Sdf.Path(str(prims[i].GetPrimPath())+'.xformOp:rotateXYZ'),
        #         value=Gf.Vec3d((current_prim[0]+scale*(self.h_option+1))%360, current_prim[1], 
        # (current_prim[2]+scale*(self.v_option+1))%360),
        #         prev=current_prim
        #         )

    def on_click2(self):
        self.state = 0
            
    def _on_update(self, event: carb.events.IEvent):
        # if error logged by carb event, stop do not update movement 
        try:
            self.udpate_movement()
        except:
            pass

    def on_shutdown(self):
        self._update_sub = None
        print("[my.rotate.extension] MyExtension shutdown")




