Colorpicker on Steroids (Blender 5)

A smart workflow enhancement for texturing and sculpting. It temporarily removes lighting and shading interference while picking colors, allowing you to sample pure, unlit values without manually tweaking your viewport settings.

## Key Features

* **Smart Shading Toggle:** Automatically switches the 3D Viewport to Flat shading and disables Cavity the moment you activate the eyedropper.
* **Context-Aware:** Works seamlessly both when hovering over UI color pickers (N-Panel, Properties) and directly within the 3D Viewport (Sculpt, Vertex Paint, Texture Paint modes).
* **Active Mesh Isolation:** When sampling directly in the 3D View, it drastically dims inactive meshes (setting Fade Inactive Alpha to 0.9) to help you focus entirely on your target geometry.
* **Auto-Restore:** The exact moment you click to confirm your color (or press Esc to cancel), your original lighting, cavity, and overlay settings are instantly brought back.
* **Custom Priority Hotkeys:** Easily change the default shortcut (mapped to 'E') directly from the Add-on Preferences. The hotkeys are registered with high priority, ensuring they override any default Blender keymap conflicts.
