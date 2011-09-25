<colors>
<<include etc/colors.conf>>
<<include etc/brewer.conf>>
blackweak = 0,0,0,100
</colors>

<fonts>
<<include etc/fonts.conf>>
</fonts>

<<include ideogram.conf>>
<<include ticks.conf>>

<image>
dir   = .
file  = circos.png
png   = yes
svg   = yes
24bit = yes
# radius of inscribed circle in image
radius         = 1500p
background     = white
angle_orientation = counterclockwise
angle_offset   = -90

auto_alpha_colors = yes
auto_alpha_steps = 5

#image_map_use      = yes
#image_map_name     = circosmap
</image>

karyotype  = karyotype.txt

chromosomes_units = 100
chromosomes_display_default = yes

<links>
<rules>
<rule>
condition       = 1
thickness = eval(_SIZE1_/1000)
</rule>
</rules>
radius          = 0.99r
crest           = 1
bezier_radius   = 0.2r
bezier_radius_purity = 0.5
ribbon          = yes
flat            = yes


stroke_color    = black
stroke_thickness= 1

#for $link in $links
<link segdup${link.id}>
show            = yes
thickness       = 5
color           = ${link.color}_a2
file            = segdup${link.id}.txt
</link>
#end for
</links>


<highlights>
z = 0
fill_color = green
<highlight>
file = highlights.txt
r0 = 1r
r1 = 1r + 100p
</highlight>
</highlights>

<<include etc/housekeeping.conf>>
