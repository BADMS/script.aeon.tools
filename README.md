script.aeon.tools


To go in Startup.xml:

	<onload condition="System.HasAddon(script.aeon.tools)">RunScript(script.aeon.tools,daemon=True)</onload>


You will need to set somewhere the following window property for daemon to choose what color you want (or 'none' for nothing).

	SetProperty(cpa_aeon_set,overall_color,home)
	or
	SetProperty(cpa_aeon_set,frequent_color,home)

	SetProperty(cfa_aeon_set,overall_color,home)
	or
	SetProperty(cfa_aeon_set,frequent_color,home)


I would set mine via Startup.xml as so:

	<onload condition="String.IsEmpty(Skin.String(aeon_background_fx))">Skin.SetString(aeon_background_fx,overall_color)</onload>
	<onload condition="String.IsEmpty(Skin.String(aeon_focus_fx))">Skin.SetString(aeon_focus_fx,overall_color)</onload>
	<onload>SetProperty(cfa_aeon_set,$INFO[Skin.String(aeon_background_fx)],home)</onload>
	<onload>SetProperty(cpa_aeon_set,$INFO[Skin.String(aeon_focus_fx)],home)</onload>
	<onload>SetProperty(cpa_aeon_fallback,,home)</onload>


You won't need to init the addon with 'firstrun' (as in mimix Startup.xml).

The daemon always processes current 7977 and current 7978, so you have color from each in aeon_tools_Colorcpa & aeon_tools_Colorcfa, plus the complimentary colors in aeon_tools_CColorcpa & aeon_tools_CColorcfa

Plus now old colors in aeon_tools_OldColorcpa & aeon_tools_OldColorcfa, plus the complimentary old colors in aeon_tools_OldCColorcpa & aeon_tools_OldCColorcfa

Have changed 'ImageUpdating' to 'aeon_tools_ImageUpdating'


Hopefully you can see what to change to work with aeon.


Basically display all fanarts or bg art via multiimage id=7977
And all poster or forefront art via multiimage id=7978

It still processes separate colors for current song poster/fan art.


And you can process any other art via say:

	<onfocus>RunScript(script.aeon.tools,info=overall_color,id='"IMAGE_TO_PROCESS"',prefix=UNIQUE_IDENTIFIER)</onfocus>
	<onfocus>RunScript(script.aeon.tools,info=frequent_color,id='"IMAGE_TO_PROCESS"',prefix=UNIQUE_IDENTIFIER)</onfocus>

	so then you will have Window(home).Property(UNIQUE_IDENTIFIER.ImageColor) & Window(home).Property(UNIQUE_IDENTIFIER.ImageCColor)

	&

	Window(home).Property(UNIQUE_IDENTIFIER.ImageOldColor) & Window(home).Property(UNIQUE_IDENTIFIER.ImageOldCColor)


Get stuck ask via gmail :-)

