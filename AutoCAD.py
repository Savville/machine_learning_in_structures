"""
AutoCAD Security Guard House Generator
=====================================
This script automates AutoCAD to create a 3D model of a security guard house
using the pyautocad library for COM interface communication.

Requirements:
- AutoCAD must be installed and running
- pip install pyautocad
- Windows OS (COM interface requirement)
"""

try:
    from pyautocad import Autocad, APoint
    import math
except ImportError:
    print("Error: pyautocad library not found. Install with: pip install pyautocad")
    exit(1)

class GuardHouseCAD:
    def __init__(self):
        """Initialize AutoCAD connection"""
        try:
            self.acad = Autocad(create_if_not_exists=True)
            self.doc = self.acad.doc
            self.model = self.acad.model
            print("✓ Connected to AutoCAD successfully")
        except Exception as e:
            print(f"✗ Failed to connect to AutoCAD: {e}")
            print("Make sure AutoCAD is running and try again.")
            exit(1)
    
    def create_layers(self):
        """Create and configure layers with specified colors"""
        print("Creating layers...")
        
        layers_config = [
            ("WALLS", 1),    # Red
            ("DOOR", 3),     # Green  
            ("WINDOWS", 5),  # Blue
            ("ROOF", 2),     # Yellow
            ("SLAB", 8)      # Dark Gray
        ]
        
        for layer_name, color_number in layers_config:
            try:
                # Create layer
                layer = self.doc.Layers.Add(layer_name)
                layer.color = color_number
                print(f"✓ Created layer: {layer_name} (Color: {color_number})")
            except:
                # Layer might already exist
                layer = self.doc.Layers.Item(layer_name)
                layer.color = color_number
                print(f"✓ Updated existing layer: {layer_name}")
    
    def set_active_layer(self, layer_name):
        """Set the active layer"""
        self.doc.ActiveLayer = self.doc.Layers.Item(layer_name)
    
    def draw_slab(self):
        """Draw the foundation slab"""
        print("Drawing slab...")
        self.set_active_layer("SLAB")
        
        # Slab corners (3.01m x 2.1m)
        points = [
            APoint(0, 0, 0),
            APoint(3.01, 0, 0),
            APoint(3.01, 2.1, 0),
            APoint(0, 2.1, 0),
            APoint(0, 0, 0)  # Close the rectangle
        ]
        
        # Draw slab outline
        for i in range(len(points) - 1):
            self.model.AddLine(points[i], points[i + 1])
    
    def draw_walls(self):
        """Draw all wall segments"""
        print("Drawing walls...")
        self.set_active_layer("WALLS")
        
        # Wall height
        h = 2.7
        
        # Vertical wall lines (corners)
        wall_lines = [
            # Corner posts
            [APoint(0, 0, 0), APoint(0, 0, h)],
            [APoint(0, 2.1, 0), APoint(0, 2.1, h)],
            [APoint(3.01, 0, 0), APoint(3.01, 0, h)],
            [APoint(3.01, 2.1, 0), APoint(3.01, 2.1, h)],
            
            # Top wall plates
            [APoint(0, 0, h), APoint(3.01, 0, h)],
            [APoint(0, 2.1, h), APoint(3.01, 2.1, h)],
            [APoint(0, 0, h), APoint(0, 2.1, h)],
            [APoint(3.01, 0, h), APoint(3.01, 2.1, h)]
        ]
        
        for start_point, end_point in wall_lines:
            self.model.AddLine(start_point, end_point)
        
        # Front wall segments (around door and window)
        front_wall_segments = [
            # Left of door
            [APoint(0, 0, 0), APoint(0.5, 0, 0)],
            [APoint(0, 0, h), APoint(0.5, 0, h)],
            [APoint(0.5, 0, 0), APoint(0.5, 0, h)],
            
            # Between door and window
            [APoint(1.4, 0, 0), APoint(1.66, 0, 0)],
            [APoint(1.4, 0, h), APoint(1.66, 0, h)],
            [APoint(1.4, 0, 0), APoint(1.4, 0, h)],
            [APoint(1.66, 0, 0), APoint(1.66, 0, h)],
            
            # Right of window
            [APoint(2.31, 0, 0), APoint(3.01, 0, 0)],
            [APoint(2.31, 0, h), APoint(3.01, 0, h)],
            [APoint(2.31, 0, 0), APoint(2.31, 0, h)],
            
            # Above door
            [APoint(0.5, 0, 2.0), APoint(1.4, 0, 2.0)],
            
            # Above window  
            [APoint(1.66, 0, 2.0), APoint(2.31, 0, 2.0)],
            
            # Below window
            [APoint(1.66, 0, 0), APoint(2.31, 0, 0)],
            [APoint(1.66, 0, 1.1), APoint(2.31, 0, 1.1)]
        ]
        
        for start_point, end_point in front_wall_segments:
            self.model.AddLine(start_point, end_point)
        
        # Side walls with window openings
        # Left wall segments
        left_wall_segments = [
            # Below window
            [APoint(0, 0, 1.1), APoint(0, 2.1, 1.1)],
            # Above window
            [APoint(0, 0, 2.0), APoint(0, 2.1, 2.0)],
            # Left of window
            [APoint(0, 0, 1.1), APoint(0, 0.72, 1.1)],
            [APoint(0, 0, 2.0), APoint(0, 0.72, 2.0)],
            [APoint(0, 0.72, 1.1), APoint(0, 0.72, 2.0)],
            # Right of window
            [APoint(0, 1.38, 1.1), APoint(0, 2.1, 1.1)],
            [APoint(0, 1.38, 2.0), APoint(0, 2.1, 2.0)],
            [APoint(0, 1.38, 1.1), APoint(0, 1.38, 2.0)]
        ]
        
        for start_point, end_point in left_wall_segments:
            self.model.AddLine(start_point, end_point)
        
        # Right wall segments (mirror of left wall)
        right_wall_segments = [
            # Below window
            [APoint(3.01, 0, 1.1), APoint(3.01, 2.1, 1.1)],
            # Above window
            [APoint(3.01, 0, 2.0), APoint(3.01, 2.1, 2.0)],
            # Left of window
            [APoint(3.01, 0, 1.1), APoint(3.01, 0.72, 1.1)],
            [APoint(3.01, 0, 2.0), APoint(3.01, 0.72, 2.0)],
            [APoint(3.01, 0.72, 1.1), APoint(3.01, 0.72, 2.0)],
            # Right of window
            [APoint(3.01, 1.38, 1.1), APoint(3.01, 2.1, 1.1)],
            [APoint(3.01, 1.38, 2.0), APoint(3.01, 2.1, 2.0)],
            [APoint(3.01, 1.38, 1.1), APoint(3.01, 1.38, 2.0)]
        ]
        
        for start_point, end_point in right_wall_segments:
            self.model.AddLine(start_point, end_point)
        
        # Back wall (solid)
        back_wall_lines = [
            [APoint(0, 2.1, 0), APoint(3.01, 2.1, 0)],
            [APoint(0, 2.1, h), APoint(3.01, 2.1, h)]
        ]
        
        for start_point, end_point in back_wall_lines:
            self.model.AddLine(start_point, end_point)
    
    def draw_door(self):
        """Draw the front door opening"""
        print("Drawing door...")
        self.set_active_layer("DOOR")
        
        # Door frame (0.9m wide, 2.0m high, 0.5m from left corner)
        door_lines = [
            [APoint(0.5, 0, 0), APoint(0.5, 0, 2.0)],    # Left frame
            [APoint(1.4, 0, 0), APoint(1.4, 0, 2.0)],    # Right frame  
            [APoint(0.5, 0, 2.0), APoint(1.4, 0, 2.0)]   # Top frame
        ]
        
        for start_point, end_point in door_lines:
            self.model.AddLine(start_point, end_point)
    
    def draw_windows(self):
        """Draw all windows"""
        print("Drawing windows...")
        self.set_active_layer("WINDOWS")
        
        # Front window (0.65m wide, 0.7m from right corner)
        front_window_lines = [
            [APoint(1.66, 0, 1.1), APoint(1.66, 0, 2.0)],   # Left frame
            [APoint(2.31, 0, 1.1), APoint(2.31, 0, 2.0)],   # Right frame
            [APoint(1.66, 0, 2.0), APoint(2.31, 0, 2.0)],   # Top frame
            [APoint(1.66, 0, 1.1), APoint(2.31, 0, 1.1)]    # Bottom frame
        ]
        
        for start_point, end_point in front_window_lines:
            self.model.AddLine(start_point, end_point)
        
        # Left side window (0.66m wide, centered)
        left_window_lines = [
            [APoint(0, 0.72, 1.1), APoint(0, 0.72, 2.0)],   # Back frame
            [APoint(0, 1.38, 1.1), APoint(0, 1.38, 2.0)],   # Front frame
            [APoint(0, 0.72, 2.0), APoint(0, 1.38, 2.0)],   # Top frame
            [APoint(0, 0.72, 1.1), APoint(0, 1.38, 1.1)]    # Bottom frame
        ]
        
        for start_point, end_point in left_window_lines:
            self.model.AddLine(start_point, end_point)
        
        # Right side window (0.66m wide, centered)
        right_window_lines = [
            [APoint(3.01, 0.72, 1.1), APoint(3.01, 0.72, 2.0)],   # Back frame
            [APoint(3.01, 1.38, 1.1), APoint(3.01, 1.38, 2.0)],   # Front frame
            [APoint(3.01, 0.72, 2.0), APoint(3.01, 1.38, 2.0)],   # Top frame
            [APoint(3.01, 0.72, 1.1), APoint(3.01, 1.38, 1.1)]    # Bottom frame
        ]
        
        for start_point, end_point in right_window_lines:
            self.model.AddLine(start_point, end_point)
    
    def draw_roof(self):
        """Draw the pyramid roof"""
        print("Drawing roof...")
        self.set_active_layer("ROOF")
        
        # Roof peak point (center of building, height 3.1m)
        roof_peak = APoint(1.505, 1.05, 3.1)
        
        # Four corner points at wall height (2.7m)
        corners = [
            APoint(0, 0, 2.7),      # Front left
            APoint(3.01, 0, 2.7),   # Front right
            APoint(0, 2.1, 2.7),    # Back left
            APoint(3.01, 2.1, 2.7)  # Back right
        ]
        
        # Draw lines from each corner to roof peak
        for corner in corners:
            self.model.AddLine(corner, roof_peak)
        
        # Draw roof base edges (wall tops)
        roof_base_lines = [
            [APoint(0, 0, 2.7), APoint(3.01, 0, 2.7)],      # Front edge
            [APoint(0, 2.1, 2.7), APoint(3.01, 2.1, 2.7)],  # Back edge
            [APoint(0, 0, 2.7), APoint(0, 2.1, 2.7)],       # Left edge
            [APoint(3.01, 0, 2.7), APoint(3.01, 2.1, 2.7)]  # Right edge
        ]
        
        for start_point, end_point in roof_base_lines:
            self.model.AddLine(start_point, end_point)
    
    def send_raw_commands(self):
        """Alternative method: Send raw AutoCAD commands"""
        print("Sending raw AutoCAD commands...")
        
        commands = [
            # Create layers
            "LAYER",
            "M", "WALLS", "C", "1", "",
            "M", "DOOR", "C", "3", "",  
            "M", "WINDOWS", "C", "5", "",
            "M", "ROOF", "C", "2", "",
            "M", "SLAB", "C", "8", "",
            "",
            
            # Draw slab
            "LAYER", "S", "SLAB", "",
            "LINE", "0,0,0", "3.01,0,0", "3.01,2.1,0", "0,2.1,0", "C", "",
            
            # Draw walls
            "LAYER", "S", "WALLS", "",
            "LINE", "0,0,0", "0,0,2.7", "",
            "LINE", "0,2.1,0", "0,2.1,2.7", "",
            "LINE", "3.01,0,0", "3.01,0,2.7", "",
            "LINE", "3.01,2.1,0", "3.01,2.1,2.7", "",
            "LINE", "0,0,2.7", "3.01,0,2.7", "",
            "LINE", "0,2.1,2.7", "3.01,2.1,2.7", "",
            "LINE", "0,0,2.7", "0,2.1,2.7", "",
            "LINE", "3.01,0,2.7", "3.01,2.1,2.7", "",
            
            # Draw door
            "LAYER", "S", "DOOR", "",
            "LINE", "0.5,0,0", "0.5,0,2", "",
            "LINE", "1.4,0,0", "1.4,0,2", "",
            "LINE", "0.5,0,2", "1.4,0,2", "",
            
            # Draw windows
            "LAYER", "S", "WINDOWS", "",
            # Front window
            "LINE", "1.66,0,1.1", "1.66,0,2.0", "",
            "LINE", "2.31,0,1.1", "2.31,0,2.0", "",
            "LINE", "1.66,0,2.0", "2.31,0,2.0", "",
            "LINE", "1.66,0,1.1", "2.31,0,1.1", "",
            
            # Left side window
            "LINE", "0,0.72,1.1", "0,0.72,2.0", "",
            "LINE", "0,1.38,1.1", "0,1.38,2.0", "",
            "LINE", "0,0.72,2.0", "0,1.38,2.0", "",
            "LINE", "0,0.72,1.1", "0,1.38,1.1", "",
            
            # Right side window
            "LINE", "3.01,0.72,1.1", "3.01,0.72,2.0", "",
            "LINE", "3.01,1.38,1.1", "3.01,1.38,2.0", "",
            "LINE", "3.01,0.72,2.0", "3.01,1.38,2.0", "",
            "LINE", "3.01,0.72,1.1", "3.01,1.38,1.1", "",
            
            # Draw roof
            "LAYER", "S", "ROOF", "",
            "LINE", "0,0,2.7", "1.505,1.05,3.1", "",
            "LINE", "3.01,0,2.7", "1.505,1.05,3.1", "",
            "LINE", "0,2.1,2.7", "1.505,1.05,3.1", "",
            "LINE", "3.01,2.1,2.7", "1.505,1.05,3.1", "",
            
            # Zoom to extents
            "ZOOM", "E", ""
        ]
        
        for command in commands:
            if command:  # Skip empty commands
                self.acad.doc.SendCommand(command + " ")
    
    def create_3d_faces(self):
        """Create 3D faces for solid visualization"""
        print("Creating 3D faces...")
        
        # Wall faces
        self.set_active_layer("WALLS")
        
        # Create 3D faces for better visualization
        try:
            # Front wall segments
            front_segments = [
                # Left segment
                [APoint(0, 0, 0), APoint(0.5, 0, 0), APoint(0.5, 0, 2.7), APoint(0, 0, 2.7)],
                # Between door and window
                [APoint(1.4, 0, 0), APoint(1.66, 0, 0), APoint(1.66, 0, 2.7), APoint(1.4, 0, 2.7)],
                # Right segment
                [APoint(2.31, 0, 0), APoint(3.01, 0, 0), APoint(3.01, 0, 2.7), APoint(2.31, 0, 2.7)]
            ]
            
            for segment in front_segments:
                self.model.Add3DFace(segment[0], segment[1], segment[2], segment[3])
            
            # Back wall (solid)
            self.model.Add3DFace(
                APoint(0, 2.1, 0), APoint(3.01, 2.1, 0), 
                APoint(3.01, 2.1, 2.7), APoint(0, 2.1, 2.7)
            )
            
        except Exception as e:
            print(f"Note: 3D faces not created - {e}")
    
    def zoom_extents(self):
        """Zoom to show all objects"""
        self.acad.doc.SendCommand("ZOOM E ")
    
    def build_complete_house(self):
        """Build the complete guard house"""
        print("\n🏠 Starting Guard House Construction...")
        print("=" * 50)
        
        try:
            # Step 1: Create layers
            self.create_layers()
            
            # Step 2: Draw components
            self.draw_slab()
            self.draw_walls() 
            self.draw_door()
            self.draw_windows()
            self.draw_roof()
            
            # Step 3: Add 3D faces for better visualization
            self.create_3d_faces()
            
            # Step 4: Set optimal view
            self.zoom_extents()
            
            print("\n✓ Guard house construction completed successfully!")
            print("✓ All layers, walls, door, windows, and roof created")
            print("✓ 3D model ready for viewing")
            
        except Exception as e:
            print(f"\n✗ Error during construction: {e}")
            print("Trying alternative raw command method...")
            self.send_raw_commands()

def alternative_command_sender():
    """Alternative approach using direct command sending"""
    try:
        acad = Autocad()
        print("✓ Connected to AutoCAD via alternative method")
        
        # Send the exact command sequence from your original specification
        command_sequence = """
LAYER
M WALLS C 1
M DOOR C 3
M WINDOWS C 5
M ROOF C 2
M SLAB C 8

LAYER
S SLAB
LINE 0,0,0 3.01,0,0 3.01,2.1,0 0,2.1,0 C

LAYER
S WALLS
LINE 0,0,0 0,0,2.7
LINE 0,2.1,0 0,2.1,2.7
LINE 3.01,0,0 3.01,0,2.7
LINE 3.01,2.1,0 3.01,2.1,2.7
LINE 0,0,2.7 3.01,0,2.7
LINE 0,2.1,2.7 3.01,2.1,2.7
LINE 0,0,2.7 0,2.1,2.7
LINE 3.01,0,2.7 3.01,2.1,2.7

LAYER
S DOOR
LINE 0.5,0,0 0.5,0,2
LINE 1.4,0,0 1.4,0,2
LINE 0.5,0,2 1.4,0,2

LAYER
S WINDOWS
LINE 1.66,0,1.1 1.66,0,2.0
LINE 2.31,0,1.1 2.31,0,2.0
LINE 1.66,0,2.0 2.31,0,2.0
LINE 1.66,0,1.1 2.31,0,1.1
LINE 0,0.72,1.1 0,0.72,2.0
LINE 0,1.38,1.1 0,1.38,2.0
LINE 0,0.72,2.0 0,1.38,2.0
LINE 0,0.72,1.1 0,1.38,1.1
LINE 3.01,0.72,1.1 3.01,0.72,2.0
LINE 3.01,1.38,1.1 3.01,1.38,2.0
LINE 3.01,0.72,2.0 3.01,1.38,2.0
LINE 3.01,0.72,1.1 3.01,1.38,1.1

LAYER
S ROOF
LINE 0,0,2.7 1.505,1.05,3.1
LINE 3.01,0,2.7 1.505,1.05,3.1
LINE 0,2.1,2.7 1.505,1.05,3.1
LINE 3.01,2.1,2.7 1.505,1.05,3.1

ZOOM E
"""
        
        # Send commands line by line
        for line in command_sequence.strip().split('\n'):
            if line.strip():
                acad.doc.SendCommand(line.strip() + " ")
        
        print("✓ All commands sent to AutoCAD successfully!")
        
    except Exception as e:
        print(f"✗ Alternative method failed: {e}")

def main():
    """Main execution function"""
    print("AutoCAD Security Guard House Generator")
    print("=" * 40)
    print("Building Specifications:")
    print("• Length: 3.01m, Width: 2.1m")
    print("• Wall Height: 2.7m, Roof Peak: 3.1m") 
    print("• Door: 0.9m × 2.0m (front)")
    print("• Windows: 0.65m × 0.9m (front), 0.66m × 0.9m (sides)")
    print("=" * 40)
    
    try:
        # Method 1: Object-oriented approach
        print("\nAttempting Method 1: Object-oriented AutoCAD automation...")
        guard_house = GuardHouseCAD()
        guard_house.build_complete_house()
        
    except Exception as e:
        print(f"\nMethod 1 failed: {e}")
        print("\nAttempting Method 2: Raw command sequence...")
        alternative_command_sender()

def print_installation_instructions():
    """Print setup instructions"""
    instructions = """
INSTALLATION & SETUP INSTRUCTIONS:
==================================

1. Install Required Python Package:
   pip install pyautocad

2. AutoCAD Requirements:
   • AutoCAD must be installed on Windows
   • AutoCAD should be running before executing this script
   • Enable COM interface in AutoCAD (usually enabled by default)

3. Running the Script:
   python autocad_guard_house.py

4. Troubleshooting:
   • If connection fails, try starting AutoCAD manually first
   • Ensure no other scripts are controlling AutoCAD
   • Check Windows UAC settings if COM access is blocked
   • Try running Python as administrator if needed

5. Alternative Manual Method:
   If automation fails, copy the AutoCAD commands from the script
   and paste them directly into AutoCAD command line.

FEATURES:
=========
• Automated layer creation with proper colors
• Complete 3D wireframe model generation
• Proper building dimensions and proportions
• Door and window openings correctly positioned
• Pyramid-style roof structure
• Automatic zoom to extents for optimal viewing
"""
    print(instructions)

if __name__ == "__main__":
    print_installation_instructions()
    print("\nPress Enter to continue with AutoCAD automation, or Ctrl+C to exit...")
    input()
    main()