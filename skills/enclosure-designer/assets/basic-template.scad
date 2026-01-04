/*
 * Basic Electronics Enclosure Template
 * OpenSCAD Parametric Design
 * 
 * Instructions:
 * 1. Modify parameters in the CONFIGURATION section
 * 2. Preview with F5
 * 3. Render with F6 (takes longer but needed for export)
 * 4. Export STL with File -> Export -> Export as STL
 */

// =============================================================================
// CONFIGURATION - Modify these values
// =============================================================================

// Interior dimensions (mm)
interior_width = 80;
interior_depth = 50;
interior_height = 25;

// Wall parameters
wall_thickness = 2.5;
bottom_thickness = 2.5;
corner_radius = 3;

// Lid parameters
lid_thickness = 2;
lid_tolerance = 0.3;  // Gap for fit
lid_lip_height = 3;

// Quality (higher = smoother, slower)
$fn = 50;

// =============================================================================
// CALCULATED VALUES
// =============================================================================

outer_width = interior_width + 2 * wall_thickness;
outer_depth = interior_depth + 2 * wall_thickness;
outer_height = interior_height + bottom_thickness;

// =============================================================================
// MODULES
// =============================================================================

module rounded_box(w, d, h, r) {
    // Box with rounded vertical edges
    minkowski() {
        cube([w - 2*r, d - 2*r, h/2]);
        cylinder(r=r, h=h/2);
    }
}

module base() {
    difference() {
        // Outer shell
        translate([corner_radius, corner_radius, 0])
            rounded_box(outer_width, outer_depth, outer_height, corner_radius);
        
        // Interior cavity
        translate([wall_thickness, wall_thickness, bottom_thickness])
            cube([interior_width, interior_depth, interior_height + 1]);
        
        // Lid recess
        translate([wall_thickness - lid_tolerance, 
                   wall_thickness - lid_tolerance, 
                   outer_height - lid_lip_height])
            cube([interior_width + 2*lid_tolerance, 
                  interior_depth + 2*lid_tolerance, 
                  lid_lip_height + 1]);
    }
}

module lid() {
    lip_width = interior_width - 1;
    lip_depth = interior_depth - 1;
    
    union() {
        // Top plate
        translate([corner_radius, corner_radius, 0])
            rounded_box(outer_width, outer_depth, lid_thickness, corner_radius);
        
        // Inner lip
        translate([wall_thickness + 0.5, wall_thickness + 0.5, -lid_lip_height + 0.5])
            difference() {
                cube([lip_width, lip_depth, lid_lip_height]);
                translate([1.5, 1.5, -0.1])
                    cube([lip_width - 3, lip_depth - 3, lid_lip_height + 1]);
            }
    }
}

module standoff(x, y, height=5, outer_d=6, inner_d=2.5) {
    // PCB mounting standoff
    translate([wall_thickness + x, wall_thickness + y, bottom_thickness])
        difference() {
            cylinder(d=outer_d, h=height);
            translate([0, 0, -0.1])
                cylinder(d=inner_d, h=height + 1);
        }
}

module vent_slot(x, y, z, length=15, width=2) {
    // Horizontal ventilation slot
    translate([x, y, z])
        hull() {
            cylinder(d=width, h=wall_thickness + 2);
            translate([0, length, 0])
                cylinder(d=width, h=wall_thickness + 2);
        }
}

module cable_hole(x, y, z, diameter=8) {
    // Cable pass-through hole
    translate([x, y, z])
        rotate([90, 0, 0])
            cylinder(d=diameter, h=wall_thickness + 2);
}

// =============================================================================
// ASSEMBLY
// =============================================================================

// Base
difference() {
    base();
    
    // Example: Add ventilation on sides
    // Left side vents
    translate([-1, 0, 0]) {
        vent_slot(0, 10, 10);
        vent_slot(0, 30, 10);
    }
    // Right side vents  
    translate([outer_width - wall_thickness - 1, 0, 0]) {
        vent_slot(0, 10, 10);
        vent_slot(0, 30, 10);
    }
    
    // Example: Cable hole at back
    cable_hole(outer_width/2, outer_depth + 1, outer_height/2);
}

// Example: Add standoffs (customize positions for your PCB)
// standoff(10, 10);
// standoff(10, 40);
// standoff(70, 10);
// standoff(70, 40);

// Lid - offset for printing
translate([outer_width + 10, 0, 0])
    lid();

// =============================================================================
// TIPS
// =============================================================================
/*
 * For STL export, render parts separately:
 * - Comment out the lid, render base, export as "base.stl"
 * - Comment out base, uncomment lid only, export as "lid.stl"
 * 
 * Or use the "!" modifier to render only one part:
 * !base();   <- Only renders base
 * !lid();    <- Only renders lid
 * 
 * Print settings recommendations:
 * - Layer height: 0.2mm
 * - Infill: 20-30%
 * - No supports needed for basic enclosure
 * - Print lid upside down (flat side on bed)
 */
