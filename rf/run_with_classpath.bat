set CP=.;
for %%j in (.\java_lib\*.jar) do ( call :set_cp %%j )
set CLASSPATH=%CP%

pybot %*

goto :eof

:set_cp	
	set CP=%CP%%CD%\%1;
goto :eof
