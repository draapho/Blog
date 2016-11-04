::获取当前路径, 并替换"\"为"\\"
@echo off 
set path=%~dp0
set pathstr=%path%
set "pathstr=%pathstr:\=\\%"
REM echo %path%
REM echo %pathstr%

::创建reg文件
del %path%\_temp.reg
@echo Windows Registry Editor Version 5.00>>_temp.reg
@echo [HKEY_CLASSES_ROOT\*\Shell\Notepad++ Here]>>_temp.reg
@echo "Icon"="%pathstr%notepad++.exe">>_temp.reg
@echo [HKEY_CLASSES_ROOT\*\Shell\Notepad++ Here\Command]>>_temp.reg
@echo @="\"%pathstr%notepad++.exe\" \"%%1\"">>_temp.reg

:: 注册.reg文件到注册表中, 然后删除
reg import _temp.reg 
del %path%\_temp.reg
