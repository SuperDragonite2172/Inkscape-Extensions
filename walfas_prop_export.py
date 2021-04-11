import os
import inkex
from inkex.command import take_snapshot

class PropExport(inkex.EffectExtension):
    

    def __init__(self):
        super(PropExport, self).__init__()
    
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--prop_scale", default="200", help="Scale of the prop on canvas")
        pars.add_argument("--prop_dpi", default="96", help="DPI of the canvas")
        pars.add_argument("--export_scales", default="50, 100, 150, 200, 250, 300, 350, 400", help="Scale(s) of the exported prop (comma separated)")
        pars.add_argument("--prop_name", default="My Prop", help="Name of the Exported Prop")
        pars.add_argument("--output_path", default=os.path.expanduser("~"), help="Output Folder")
        pars.add_argument("--overwrite", type=inkex.Boolean, help="Overwrite existing exports?")
    
    def effect(self):
        # If the output path doesn't exist, create it.
        if not os.path.isdir(self.options.output_path):
            os.makedirs(self.options.output_path)
        
        # Parse the arguments passed and store them.
        start_scale = self.options.prop_scale
        start_dpi = self.options.prop_dpi
        end_scales = self.options.export_scales
        end_scales = list(map(str.strip, end_scales.split(",")))
        prop_name = self.options.prop_name
        overwrite = self.options.overwrite

        # Calculate the export DPIs from the sizes.
        while len(end_scales) > 0:
            export_scale = end_scales.pop(0)
            export_dpi = (str((int(export_scale) / int(start_scale)) * int(start_dpi)))
        
            export_name = prop_name + "_" + export_scale
            if not os.path.exists(export_name) or overwrite:
                take_snapshot(self.svg, self.options.output_path, export_name, ext = 'png', dpi = export_dpi)
                os.remove(self.options.output_path + "\\" + export_name + ".svg")

if __name__ == "__main__":
    PropExport().run()