import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, StringProperty

def get_enum_cameras(self, context):
    result = []
    for obj in context.scene.objects:
        if obj.type == 'CAMERA':
            result.append((obj.name, obj.name, ''))
    if(len(result)!=0): return result
    else: return [('None', 'None', '')]

# Classes
class OctaneManageImager(Operator):
    bl_label = 'Imager (Preview)'
    bl_idname = 'octane.manage_imager'
    bl_options = {'REGISTER', 'UNDO'}
    
    def draw(self, context):
        oct_cam = context.scene.oct_view_cam
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene.octane, "hdr_tonemap_preview_enable", text="Enable Camera Imager")
        col.prop(context.scene.octane, "use_preview_setting_for_camera_imager")

        col = layout.column(align=True)
        col.enabled = (context.scene.octane.hdr_tonemap_preview_enable and context.scene.octane.use_preview_setting_for_camera_imager)
        col.prop(oct_cam, "camera_imager_order")
        col = layout.column(align=True)
        col.enabled = (context.scene.octane.hdr_tonemap_preview_enable and context.scene.octane.use_preview_setting_for_camera_imager)
        col.prop(oct_cam, "response_type")
        col = layout.column(align=True)
        col.enabled = (context.scene.octane.hdr_tonemap_preview_enable and context.scene.octane.use_preview_setting_for_camera_imager)
        col.prop(oct_cam, "white_balance")
        col = layout.column(align=True)
        col.enabled = (context.scene.octane.hdr_tonemap_preview_enable and context.scene.octane.use_preview_setting_for_camera_imager)
        col.prop(oct_cam, "exposure")
        col.prop(oct_cam, "gamma")
        col.prop(oct_cam, "vignetting")
        col.prop(oct_cam, "saturation")
        col.prop(oct_cam, "white_saturation")
        col.prop(oct_cam, "hot_pix")
        col.prop(oct_cam, "min_display_samples")
        col.prop(oct_cam, "highlight_compression")
        col.prop(oct_cam, "max_tonemap_interval")
        col.prop(oct_cam, "dithering")
        col.prop(oct_cam, "premultiplied_alpha")
        col.prop(oct_cam, "neutral_response")
        col.prop(oct_cam, "disable_partial_alpha")
        #col.prop(oct_cam, "custom_lut")
        #col.prop(oct_cam, "lut_strength")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class OctaneManagePostprocess(Operator):
    bl_label = 'Post Processing'
    bl_idname = 'octane.manage_postprocess'
    bl_options = {'REGISTER', 'UNDO'}
    
    def draw(self, context):
        oct_cam = context.scene.oct_view_cam
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene.oct_view_cam, "postprocess", text="Enable Postprocess")
        col.prop(context.scene.octane, "use_preview_post_process_setting")
        col = layout.column(align=True)
        col.enabled = (context.scene.oct_view_cam.postprocess and context.scene.octane.use_preview_post_process_setting)
        col.prop(oct_cam, "cut_off")
        col.prop(oct_cam, "bloom_power")
        col.prop(oct_cam, "glare_power")
        col = layout.column(align=True)
        col.enabled = (context.scene.oct_view_cam.postprocess and context.scene.octane.use_preview_post_process_setting)
        col.prop(oct_cam, "glare_ray_count")
        col.prop(oct_cam, "glare_angle")
        col.prop(oct_cam, "glare_blur")
        col.prop(oct_cam, "spectral_intencity")
        col.prop(oct_cam, "spectral_shift")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class OctaneManageDenoiser(Operator):
    bl_label = 'AI Denoiser'
    bl_idname = 'octane.manage_denoiser'
    bl_options = {'REGISTER', 'UNDO'}
    
    def draw(self, context):
        oct_cam = context.scene.oct_view_cam
        view_layer = context.window.view_layer
        layout = self.layout
        col = layout.column(align=True)
        col.prop(oct_cam, 'enable_denoising', text='Enable Denosier')
        col.prop(view_layer, "use_pass_oct_denoise_beauty", text="Enable Beauty Pass")
        
        col = layout.column(align=True)
        col.enabled = (oct_cam.enable_denoising and view_layer.use_pass_oct_denoise_beauty)
        col.label(text="Spectral AI Denoiser")
        col.prop(oct_cam, 'denoise_volumes')
        col.prop(oct_cam, 'denoise_on_completion')
        col.prop(oct_cam, 'min_denoiser_samples')
        col.prop(oct_cam, 'max_denoiser_interval')
        col.prop(oct_cam, 'denoiser_blend')

        col = layout.column(align=True)
        col.enabled = (oct_cam.enable_denoising and view_layer.use_pass_oct_denoise_beauty)
        col.label(text="AI Up-Sampler")
        col.prop(oct_cam.ai_up_sampler, 'sample_mode')
        col.prop(oct_cam.ai_up_sampler, 'enable_ai_up_sampling')
        col.prop(oct_cam.ai_up_sampler, 'up_sampling_on_completion')
        col.prop(oct_cam.ai_up_sampler, 'min_up_sampler_samples')
        col.prop(oct_cam.ai_up_sampler, 'max_up_sampler_interval')

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class OctaneManagePasses(Operator):
    bl_label = 'Render Passes'
    bl_idname = 'octane.manage_render_passes'
    bl_options = {'REGISTER', 'UNDO'}

    passes: EnumProperty(items=[
        ('Beauty', 'Beauty', ''),
        ('Denoiser', 'Denoiser', ''),
        ('Post processing', 'Post processing', ''),
        ('Render layer', 'Render layer', ''),
        ('Lighting', 'Lighting', ''),
        ('Cryptomatte', 'Cryptomatte', ''),
        ('Info', 'Info', ''),
        ('Material', 'Material', ''),
    ], name='Passes', default='Beauty')
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        scene = context.scene
        rd = scene.render
        view_layer = context.view_layer
        octane_view_layer = view_layer.octane

        layout.prop(self, 'passes')
        layout.separator()

        if(self.passes == 'Beauty'):
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_beauty")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_emitters")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_env")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_sss")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_shadow")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_irradiance")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_dir")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_noise")      
            layout.row().separator()
            split = layout.split(factor=1)
            split.use_property_split = False
            row = split.row(align=True)
            row.prop(view_layer, "use_pass_oct_diff", text="Diffuse", toggle=True)
            row.prop(view_layer, "use_pass_oct_diff_dir", text="Direct", toggle=True)
            row.prop(view_layer, "use_pass_oct_diff_indir", text="Indirect", toggle=True)        
            row.prop(view_layer, "use_pass_oct_diff_filter", text="Filter", toggle=True)         
            layout.row().separator()
            split = layout.split(factor=1)
            split.use_property_split = False
            row = split.row(align=True)
            row.prop(view_layer, "use_pass_oct_reflect", text="Reflection", toggle=True)
            row.prop(view_layer, "use_pass_oct_reflect_dir", text="Direct", toggle=True)
            row.prop(view_layer, "use_pass_oct_reflect_indir", text="Indirect", toggle=True)        
            row.prop(view_layer, "use_pass_oct_reflect_filter", text="Filter", toggle=True)     
            layout.row().separator()
            split = layout.split(factor=1)
            split.use_property_split = False
            row = split.row(align=True)
            row.prop(view_layer, "use_pass_oct_refract", text="Refraction", toggle=True)
            row.prop(view_layer, "use_pass_oct_refract_filter", text="Refract Filter", toggle=True)
            layout.row().separator()
            split = layout.split(factor=1)
            split.use_property_split = False
            row = split.row(align=True)
            row.prop(view_layer, "use_pass_oct_transm", text="Transmission", toggle=True)
            row.prop(view_layer, "use_pass_oct_transm_filter", text="Transm Filter", toggle=True)        
            layout.row().separator()
            split = layout.split(factor=1)
            split.use_property_split = False
            row = split.row(align=True)
            row.prop(view_layer, "use_pass_oct_volume", text="Volume", toggle=True)
            row.prop(view_layer, "use_pass_oct_vol_mask", text="Mask", toggle=True)
            row.prop(view_layer, "use_pass_oct_vol_emission", text="Emission", toggle=True)        
            row.prop(view_layer, "use_pass_oct_vol_z_front", text="ZFront", toggle=True)
            row.prop(view_layer, "use_pass_oct_vol_z_back", text="ZBack", toggle=True)
        elif(self.passes == 'Denoiser'):
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_denoise_beauty", text="Beauty")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_denoise_diff_dir", text="DiffDir")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_denoise_diff_indir", text="DiffIndir")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_denoise_reflect_dir", text="ReflectDir")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_denoise_reflect_indir", text="ReflectIndir")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_denoise_emission", text="Emission")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_denoise_remainder", text="Remainder")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_denoise_vol", text="Volume")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_denoise_vol_emission", text="VolEmission")
        elif(self.passes == 'Post processing'):
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_postprocess", text="Post processing")
            col = flow.column()
            col.prop(octane_view_layer, "pass_pp_env")
        elif(self.passes == 'Render layer'):
            flow = layout.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_layer_shadows", text="Shadow")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_layer_black_shadow", text="BlackShadow")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_layer_reflections", text="Reflections")
        elif(self.passes == 'Lighting'):
            flow = layout.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_ambient_light", text="Ambient")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_ambient_light_dir", text="Direct")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_ambient_light_indir", text="Indirect")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_sunlight", text="Sunlight")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_sunlight_dir", text="Direct")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_sunlight_indir", text="Indirect")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_pass_1", text="Light Pass 1")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_dir_pass_1", text="Direct")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_indir_pass_1", text="Indirect")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_pass_2", text="Light Pass 2")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_dir_pass_2", text="Direct")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_indir_pass_2", text="Indirect")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_pass_3", text="Light Pass 3")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_dir_pass_3", text="Direct")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_indir_pass_3", text="Indirect")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_pass_4", text="Light Pass 4")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_dir_pass_4", text="Direct")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_indir_pass_4", text="Indirect")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_pass_5", text="Light Pass 5")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_dir_pass_5", text="Direct")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_indir_pass_5", text="Indirect")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_pass_6", text="Light Pass 6")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_dir_pass_6", text="Direct")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_indir_pass_6", text="Indirect")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_pass_7", text="Light Pass 7")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_dir_pass_7", text="Direct")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_indir_pass_7", text="Indirect")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_pass_8", text="Light Pass 8")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_dir_pass_8", text="Direct")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_light_indir_pass_8", text="Indirect")
        elif(self.passes == 'Cryptomatte'):
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_crypto_instance_id", text="Instance ID")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_crypto_mat_node_name", text="MatNodeName")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_crypto_mat_node", text="MatNode")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_crypto_mat_pin_node", text="MatPinNode")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_crypto_obj_node_name", text="ObjNodeName")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_crypto_obj_node", text="ObjNode")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_crypto_obj_pin_node", text="ObjPinNode")
            layout.row().separator()
            row = layout.row(align=True)
            row.prop(octane_view_layer, "cryptomatte_pass_channels")
            row = layout.row(align=True)
            row.prop(octane_view_layer, "cryptomatte_seed_factor")
        elif(self.passes == 'Info'):
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_z_depth")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_position")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_uv")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_tex_tangent")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_motion_vector")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_mat_id")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_obj_id")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_obj_layer_color")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_baking_group_id")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_light_pass_id")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_render_layer_id")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_render_layer_mask")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_wireframe")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_info_ao")
            layout.row().separator()
            split = layout.split(factor=0.15)
            split.use_property_split = False
            split.label(text="Normal")
            row = split.row(align=True)       
            row.prop(view_layer, "use_pass_oct_info_geo_normal", text="Geometric", toggle=True)         
            row.prop(view_layer, "use_pass_oct_info_smooth_normal", text="Smooth", toggle=True)
            row.prop(view_layer, "use_pass_oct_info_shading_normal", text="Shading", toggle=True)
            row.prop(view_layer, "use_pass_oct_info_tangent_normal", text="Tangent", toggle=True)
            layout.row().separator()
            row = layout.row(align=True)
            row.prop(octane_view_layer, "info_pass_max_samples")
            row = layout.row(align=True)
            row.prop(octane_view_layer, "info_pass_sampling_mode")
            row = layout.row(align=True)
            row.prop(octane_view_layer, "info_pass_z_depth_max")
            row = layout.row(align=True)
            row.prop(octane_view_layer, "info_pass_uv_max")
            row = layout.row(align=True)
            row.prop(octane_view_layer, "info_pass_uv_coordinate_selection")
            row = layout.row(align=True)
            row.prop(octane_view_layer, "info_pass_max_speed")
            row = layout.row(align=True)
            row.prop(octane_view_layer, "info_pass_ao_distance")                        
            row = layout.row(align=True)
            row.prop(octane_view_layer, "info_pass_alpha_shadows") 
        elif(self.passes == 'Material'):
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_mat_opacity")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_mat_roughness")
            col = flow.column()
            col.prop(view_layer, "use_pass_oct_mat_ior")

            layout.row().separator()

            split = layout.split(factor=0.15)
            split.use_property_split = False
            split.label(text="Filter")
            row = split.row(align=True)       
            row.prop(view_layer, "use_pass_oct_mat_diff_filter_info", text="Diffuse", toggle=True)         
            row.prop(view_layer, "use_pass_oct_mat_reflect_filter_info", text="Reflection", toggle=True)
            row.prop(view_layer, "use_pass_oct_mat_refract_filter_info", text="Refraction", toggle=True)
            row.prop(view_layer, "use_pass_oct_mat_transm_filter_info", text="Transmission", toggle=True)

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class OctaneManageLayers(Operator):
    bl_label = 'Render Layers'
    bl_idname = 'octane.manage_render_layers'
    bl_options = {'REGISTER', 'UNDO'}
    
    def draw(self, context):
        s_octane = context.scene.octane
        layout = self.layout
        col = layout.column(align=True)
        col.prop(s_octane, "layers_enable", text="Enable Render Layers")
        col = layout.column(align=True)
        col.enabled = s_octane.layers_enable
        col.prop(s_octane, "layers_mode")
        col.prop(s_octane, "layers_current")
        col.prop(s_octane, "layers_invert")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class OctaneCamerasManager(Operator):
    bl_label = 'Cameras Manager'
    bl_idname = 'octane.cameras_manager'
    bl_options = {'REGISTER', 'UNDO'}

    cameras: EnumProperty(
        name='Cameras',
        items=get_enum_cameras
    )
    
    octane_cam_settings: EnumProperty(
        name='Octane',
        items=[
            ('Imager', 'Imager (Render)', ''),
            ('Depth of field', 'Depth of field', ''),
            ('Distortion', 'Distortion', ''),
            ('Stereo', 'Stereo', ''),
            ('Baking', 'Baking', ''),
            ('OSL Camera', 'OSL Camera', '')
        ],
        default='Imager'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'cameras', text='')
        layout.use_property_split = True
        if(self.cameras != 'None' and self.cameras != None and self.cameras != ''):
            cam = context.scene.objects[self.cameras].data
            oct_cam = cam.octane

            # Lens
            layout.label(text='Lens')
            col = layout.column()
            col.prop(cam, "type")
            col.separator()
            if cam.type == 'PERSP':
                col = layout.column()
                if cam.lens_unit == 'MILLIMETERS':
                    col.prop(cam, "lens")
                elif cam.lens_unit == 'FOV':
                    col.prop(cam, "angle")
                col.prop(cam, "lens_unit")
            elif cam.type == 'ORTHO':
                col.prop(cam, "ortho_scale")
            elif cam.type == 'PANO':
                engine = context.engine
                if engine == 'CYCLES':
                    ccam = cam.cycles
                    col.prop(ccam, "panorama_type")
                    if ccam.panorama_type == 'FISHEYE_EQUIDISTANT':
                        col.prop(ccam, "fisheye_fov")
                    elif ccam.panorama_type == 'FISHEYE_EQUISOLID':
                        col.prop(ccam, "fisheye_lens", text="Lens")
                        col.prop(ccam, "fisheye_fov")
                    elif ccam.panorama_type == 'EQUIRECTANGULAR':
                        sub = col.column(align=True)
                        sub.prop(ccam, "latitude_min", text="Latitude Min")
                        sub.prop(ccam, "latitude_max", text="Max")
                        sub = col.column(align=True)
                        sub.prop(ccam, "longitude_min", text="Longitude Min")
                        sub.prop(ccam, "longitude_max", text="Max")
                elif engine in {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}:
                    if cam.lens_unit == 'MILLIMETERS':
                        col.prop(cam, "lens")
                    elif cam.lens_unit == 'FOV':
                        col.prop(cam, "angle")
                    col.prop(cam, "lens_unit")

            col = layout.column()
            col.separator()
            sub = col.column(align=True)
            sub.prop(cam, "shift_x", text="Shift X")
            sub.prop(cam, "shift_y", text="Y")
            col.separator()
            sub = col.column(align=True)
            sub.prop(cam, "clip_start", text="Clip Start")
            sub.prop(cam, "clip_end", text="End")
            
            # Sensor
            layout.label(text='Sensor')
            col = layout.column()
            col.prop(cam, "sensor_fit")

            if cam.sensor_fit == 'AUTO':
                col.prop(cam, "sensor_width", text="Size")
            else:
                sub = col.column(align=True)
                sub.active = cam.sensor_fit == 'HORIZONTAL'
                sub.prop(cam, "sensor_width", text="Width")

                sub = col.column(align=True)
                sub.active = cam.sensor_fit == 'VERTICAL'
                sub.prop(cam, "sensor_height", text="Height")

            # Dropdown Cam settings
            layout.label(text='Octane')
            layout.prop(self, 'octane_cam_settings', text='')

            if(self.octane_cam_settings == 'Imager'):
                box = layout.box()
                sub = box.column(align=True)
                sub.prop(context.scene.octane, "hdr_tonemap_render_enable", text="Enable Camera Imager")
                sub.operator(OctaneCopyCameraSettings.bl_idname, text='Copy settings to Imager (Preview)').camera = self.cameras

                sub = box.row()
                sub.enabled = context.scene.octane.hdr_tonemap_render_enable
                sub.prop(oct_cam, "camera_imager_order")

                sub = box.row()
                sub.enabled = context.scene.octane.hdr_tonemap_render_enable
                sub.prop(oct_cam, "response_type")

                sub = box.column(align=True)
                sub.enabled = context.scene.octane.hdr_tonemap_render_enable
                sub.prop(oct_cam, "white_balance")
                sub.prop(oct_cam, "exposure")
                sub.prop(oct_cam, "gamma")
                sub.prop(oct_cam, "vignetting")
                sub.prop(oct_cam, "saturation")
                sub.prop(oct_cam, "white_saturation")
                sub.prop(oct_cam, "hot_pix")
                sub.prop(oct_cam, "min_display_samples")
                sub.prop(oct_cam, "highlight_compression")
                sub.prop(oct_cam, "max_tonemap_interval")
                sub.prop(oct_cam, "dithering")
                sub.prop(oct_cam, "premultiplied_alpha")
                sub.prop(oct_cam, "neutral_response")
                sub.prop(oct_cam, "disable_partial_alpha")
                #sub.prop(oct_cam, "custom_lut")
                #sub.prop(oct_cam, "lut_strength")
            elif(self.octane_cam_settings == 'Depth of field'):
                box = layout.box()
                sub = box.column(align=True)
                sub.prop(oct_cam, "autofocus")
                sub = box.row(align=True)
                sub.active = oct_cam.autofocus is False
                sub.prop(cam.dof, "focus_object", text="")
                sub = box.row(align=True)
                sub.active = oct_cam.autofocus is False and cam.dof.focus_object is None
                sub.prop(cam.dof, "focus_distance", text="Distance")
                sub = box.column(align=True)
                sub.prop(oct_cam, "aperture")
                sub.prop(oct_cam, "aperture_aspect")
                sub.prop(oct_cam, "aperture_edge")        
                sub.prop(oct_cam, "bokeh_sidecount")
                sub.prop(oct_cam, "bokeh_rotation")
                sub.prop(oct_cam, "bokeh_roundedness")
            elif(self.octane_cam_settings == 'Distortion'):
                box = layout.box()
                sub = box.column(align=True)
                sub.active = (cam.type == 'PANO')
                sub.prop(oct_cam, "pan_mode")
                sub.prop(oct_cam, "fov_x")
                sub.prop(oct_cam, "fov_y")
                sub.prop(oct_cam, "keep_upright")
                sub = box.column(align=True)
                sub.active = (cam.type != 'PANO')
                sub.prop(oct_cam, "distortion")
                sub.prop(oct_cam, "pixel_aspect")
                sub.prop(oct_cam, "persp_corr")
                sub = box.row(align=True)
                sub.prop(oct_cam, "use_fstop")
                sub.prop(oct_cam, "fstop") 
            elif(self.octane_cam_settings == 'Stereo'):
                box = layout.box()
                col = box.column(align=True)
                sub = box.row()
                sub.active = (cam.type != 'PANO')
                sub.prop(oct_cam, "stereo_mode")
                sub = box.row()
                #sub.active = (cam.type == 'PANO' or oct_cam.stereo_mode != '1')
                sub.prop(oct_cam, "stereo_out")
                sub = box.row()
                #sub.active = (cam.type == 'PANO' or oct_cam.stereo_mode != '1')
                sub.prop(oct_cam, "stereo_dist")
                sub.prop(oct_cam, "stereo_swap_eyes")
                sub = box.column(align=True)
                #sub.active = (cam.type == 'PANO')
                sub.prop(oct_cam, "stereo_dist_falloff")
                sub.prop(oct_cam, "blackout_lat")
                col = box.column(align=True)
                #col.active = (cam.type == 'PANO' or oct_cam.stereo_mode != '1')
                sub = col.row()
                sub.prop(oct_cam, "left_filter")
                sub = col.row()
                sub.prop(oct_cam, "right_filter")
            elif(self.octane_cam_settings == 'Baking'):
                box = layout.box()
                col = box.column(align=True)
                sub = col.row(align=True)
                sub.prop(oct_cam, "baking_camera")
                sub = col.row(align=True)
                sub.active = (oct_cam.baking_camera == True)
                sub.prop(oct_cam, "baking_revert")
                sub = col.row(align=True)
                sub.active = (oct_cam.baking_camera == True)
                sub.prop(oct_cam, "baking_use_position")
                sub = col.row(align=True)
                sub.active = (oct_cam.baking_camera == True)
                sub.prop(oct_cam, "baking_bkface_culling")
                sub = col.row(align=True)
                sub.active = (oct_cam.baking_camera == True)
                sub.prop(oct_cam, "baking_tolerance")
                sub = col.row(align=True)
                sub.active = (oct_cam.baking_camera == True)
                sub.prop(oct_cam, "baking_group_id")
                sub = col.row(align=True)
                sub.active = (oct_cam.baking_camera == True)
                sub.prop(oct_cam, "baking_padding")
                sub = col.row(align=True)
                sub.active = (oct_cam.baking_camera == True)
                sub.prop(oct_cam, "baking_uv_set")
            elif(self.octane_cam_settings == 'OSL Camera'):
                box = layout.box()
                col = box.column(align = True)
                sub = col.row(align = True)
                sub.prop_search(oct_cam.osl_camera_node_collections, "osl_camera_material_tree", bpy.data, "materials")
                sub = col.row(align = True)        
                sub.prop_search(oct_cam.osl_camera_node_collections, "osl_camera_node", oct_cam.osl_camera_node_collections, "osl_camera_nodes")        
                sub.operator('update.osl_camera_nodes', text = 'Update')

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        if(context.active_object!=None):
            if(context.active_object.type=='CAMERA'):
                self.cameras = context.active_object.name
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
class OctaneCopyCameraSettings(Operator):
    bl_label = 'Copy Camera Settings'
    bl_idname = 'octane.copy_camera_settings'
    bl_options = {'REGISTER', 'UNDO'}

    camera: StringProperty(
        default='Unknown'
    )

    def execute(self, context):
        oct_view = context.scene.oct_view_cam
        oct_cam = context.scene.objects[self.camera].data.octane

        oct_view.white_balance = oct_cam.white_balance
        oct_view.exposure = oct_cam.exposure
        oct_view.gamma = oct_cam.gamma
        oct_view.vignetting = oct_cam.vignetting
        oct_view.saturation = oct_cam.saturation
        oct_view.white_saturation = oct_cam.white_saturation
        oct_view.hot_pix = oct_cam.hot_pix
        oct_view.min_display_samples = oct_cam.min_display_samples
        oct_view.highlight_compression = oct_cam.highlight_compression
        oct_view.max_tonemap_interval = oct_cam.max_tonemap_interval
        oct_view.dithering = oct_cam.dithering
        oct_view.premultiplied_alpha = oct_cam.premultiplied_alpha
        oct_view.neutral_response = oct_cam.neutral_response
        oct_view.disable_partial_alpha = oct_cam.disable_partial_alpha

        return {'FINISHED'}